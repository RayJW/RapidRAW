import React, { useState, useEffect, useCallback, useRef, Fragment } from 'react';
import { useTranslation } from 'react-i18next';
import { invoke } from '@tauri-apps/api/core';
import throttle from 'lodash.throttle';
import { Check, RotateCcw, Grid3X3, Eye, EyeOff, Info, ZoomIn, ZoomOut, Maximize, Trash2, Minus } from 'lucide-react';

import { TextColors, TextVariants, TextWeights } from '../../types/typography';
import { AnimatePresence, motion } from 'framer-motion';
import { Stage, Layer, Line, Circle } from 'react-konva';
import { v4 as uuidv4 } from 'uuid';
import { toast } from 'react-toastify';
import clsx from 'clsx';

import Button from '../ui/Button';
import Slider from '../ui/Slider';
import Text from '../ui/Text';
import { Adjustments, GuideLine, GuideOrientation, Coord } from '../../utils/adjustments';
import { useEditorStore } from '../../store/useEditorStore';

interface GeometryParams {
  distortion: number;
  vertical: number;
  horizontal: number;
  rotate: number;
  aspect: number;
  scale: number;
  x_offset: number;
  y_offset: number;
  lens_distortion_amount: number;
  lens_vignette_amount: number;
  lens_tca_amount: number;
  lens_dist_k1: number;
  lens_dist_k2: number;
  lens_dist_k3: number;
  lens_model: number;
  tca_vr: number;
  tca_vb: number;
  vig_k1: number;
  vig_k2: number;
  vig_k3: number;
  lens_distortion_enabled: boolean;
  lens_tca_enabled: boolean;
  lens_vignette_enabled: boolean;
  guided_lines: GuideLine[];
  guided_perspective_enabled: boolean;
}

type TransformParams = Omit<
  GeometryParams,
  | 'lens_distortion_amount'
  | 'lens_vignette_amount'
  | 'lens_tca_amount'
  | 'lens_dist_k1'
  | 'lens_dist_k2'
  | 'lens_dist_k3'
  | 'lens_model'
  | 'tca_vr'
  | 'tca_vb'
  | 'vig_k1'
  | 'vig_k2'
  | 'vig_k3'
  | 'lens_distortion_enabled'
  | 'lens_tca_enabled'
  | 'lens_vignette_enabled'
  | 'guided_lines'
  | 'guided_perspective_enabled'
>;

interface TransformModalProps {
  isOpen: boolean;
  onClose(): void;
  onApply(newAdjustments: Partial<Adjustments>): void;
  currentAdjustments: Adjustments;
}

const DEFAULT_PARAMS: TransformParams = {
  distortion: 0,
  vertical: 0,
  horizontal: 0,
  rotate: 0,
  aspect: 0,
  scale: 100,
  x_offset: 0,
  y_offset: 0,
};

const SLIDER_DIVISOR = 100.0;
const IDENTITY_3X3 = [1, 0, 0, 0, 1, 0, 0, 0, 1];

function multiply3x3(a: number[], b: number[]): number[] {
  if (!a || !b) return IDENTITY_3X3;
  const out = [0, 0, 0, 0, 0, 0, 0, 0, 0];
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      out[i * 3 + j] = a[i * 3 + 0] * b[0 * 3 + j] + a[i * 3 + 1] * b[1 * 3 + j] + a[i * 3 + 2] * b[2 * 3 + j];
    }
  }
  return out;
}

function invert3x3(h: number[]): number[] {
  if (!h) return IDENTITY_3X3;
  const a = h[0],
    b = h[1],
    c = h[2],
    d = h[3],
    e = h[4],
    f = h[5],
    g = h[6],
    hh = h[7],
    i = h[8];
  const A = e * i - f * hh,
    B = f * g - d * i,
    C = d * hh - e * g;
  const D = c * hh - b * i,
    E = a * i - c * g,
    F = b * g - a * hh;
  const G = b * f - c * e,
    H = c * d - a * f,
    I = a * e - b * d;
  const det = a * A + b * B + c * C;
  if (Math.abs(det) < 1e-15) return IDENTITY_3X3;
  const inv = 1.0 / det;
  return [A * inv, D * inv, G * inv, B * inv, E * inv, H * inv, C * inv, F * inv, I * inv];
}

function project3x3(h: number[], x: number, y: number): { x: number; y: number } {
  if (!h) return { x, y };
  const W = h[6] * x + h[7] * y + h[8];
  if (Math.abs(W) < 1e-12) return { x, y };
  return {
    x: (h[0] * x + h[1] * y + h[2]) / W,
    y: (h[3] * x + h[4] * y + h[5]) / W,
  };
}

function orientPoint(x: number, y: number, w: number, h: number, steps: number) {
  const s = ((steps % 4) + 4) % 4;
  if (s === 0) return { x, y };
  if (s === 1) return { x: h - y, y: x };
  if (s === 2) return { x: w - x, y: h - y };
  return { x: y, y: w - x };
}

function unorientPoint(x: number, y: number, w: number, h: number, steps: number) {
  const s = ((steps % 4) + 4) % 4;
  const inv = (4 - s) % 4;
  return orientPoint(x, y, w, h, inv);
}

const CustomGrid = ({ denseVisible, ruleOfThirdsVisible }: { denseVisible: boolean; ruleOfThirdsVisible: boolean }) => (
  <div className="absolute inset-0 pointer-events-none w-full h-full z-10">
    <div
      className={clsx(
        'absolute inset-0 w-full h-full transition-opacity duration-300 ease-in-out',
        ruleOfThirdsVisible ? 'opacity-100' : 'opacity-0',
      )}
    >
      <div className="absolute top-0 bottom-0 border-l border-white/40 left-1/3" />
      <div className="absolute top-0 bottom-0 border-l border-white/40 left-2/3" />
      <div className="absolute left-0 right-0 border-t border-white/40 top-1/3" />
      <div className="absolute left-0 right-0 border-t border-white/40 top-2/3" />
    </div>

    <div
      className={clsx(
        'absolute inset-0 w-full h-full transition-opacity duration-500 ease-in-out',
        denseVisible ? 'opacity-100' : 'opacity-0',
      )}
    >
      {[...Array(17)].map((_, i) => (
        <div
          key={`v-${i}`}
          className="absolute top-0 bottom-0 border-l border-white/40"
          style={{ left: `${(i + 1) * 5.555}%` }}
        />
      ))}
      {[...Array(17)].map((_, i) => (
        <div
          key={`h-${i}`}
          className="absolute left-0 right-0 border-t border-white/40"
          style={{ top: `${(i + 1) * 5.555}%` }}
        />
      ))}
    </div>
  </div>
);

export default function TransformModal({ isOpen, onClose, onApply, currentAdjustments }: TransformModalProps) {
  const { t } = useTranslation();
  const selectedImage = useEditorStore((s) => s.selectedImage);

  const [params, setParams] = useState<TransformParams>(DEFAULT_PARAMS);
  const [guidedLines, setGuidedLines] = useState<GuideLine[]>([]);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const [isApplying, setIsApplying] = useState(false);
  const [showGrid, setShowGrid] = useState(true);
  const [isCompareActive, setIsCompareActive] = useState(false);
  const [isInteracting, setIsInteracting] = useState(false);

  const [selectedGuideId, setSelectedGuideId] = useState<string | null>(null);
  const [draftLine, setDraftLine] = useState<{ p1: Coord; p2: Coord } | null>(null);

  const [renderDims, setRenderDims] = useState({ width: 0, height: 0 });
  const [forwardH, setForwardH] = useState<number[]>(IDENTITY_3X3);
  const [invH, setInvH] = useState<number[]>(IDENTITY_3X3);

  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);

  const containerRef = useRef<HTMLDivElement>(null);
  const imgRef = useRef<HTMLImageElement>(null);
  const lastMousePos = useRef({ x: 0, y: 0 });

  const [isMounted, setIsMounted] = useState(false);
  const [show, setShow] = useState(false);

  const Ow = selectedImage?.width || 1920;
  const Oh = selectedImage?.height || 1080;
  const orientationSteps = currentAdjustments.orientationSteps || 0;
  const isSwapped = orientationSteps % 2 !== 0;
  const Dw = isSwapped ? Oh : Ow;
  const Dh = isSwapped ? Ow : Oh;
  const flipH = currentAdjustments.flipHorizontal ?? false;
  const flipV = currentAdjustments.flipVertical ?? false;

  const measureImage = useCallback(() => {
    if (imgRef.current) {
      setRenderDims({
        width: imgRef.current.clientWidth,
        height: imgRef.current.clientHeight,
      });
    }
  }, []);

  useEffect(() => {
    const el = imgRef.current;
    if (!el || typeof ResizeObserver === 'undefined') return;
    const ro = new ResizeObserver(measureImage);
    ro.observe(el);
    return () => ro.disconnect();
  }, [measureImage, previewUrl]);

  useEffect(() => {
    if (!isDragging) return;
    const handleWindowMouseMove = (e: MouseEvent) => {
      const dx = e.clientX - lastMousePos.current.x;
      const dy = e.clientY - lastMousePos.current.y;
      setPan((prev) => ({ x: prev.x + dx, y: prev.y + dy }));
      lastMousePos.current = { x: e.clientX, y: e.clientY };
    };
    const handleWindowMouseUp = () => setIsDragging(false);
    window.addEventListener('mousemove', handleWindowMouseMove);
    window.addEventListener('mouseup', handleWindowMouseUp);
    return () => {
      window.removeEventListener('mousemove', handleWindowMouseMove);
      window.removeEventListener('mouseup', handleWindowMouseUp);
    };
  }, [isDragging]);

  useEffect(() => {
    const handleDragEndGlobal = () => {
      if (isInteracting) setIsInteracting(false);
    };
    if (isInteracting) {
      window.addEventListener('mouseup', handleDragEndGlobal);
      window.addEventListener('touchend', handleDragEndGlobal);
    }
    return () => {
      window.removeEventListener('mouseup', handleDragEndGlobal);
      window.removeEventListener('touchend', handleDragEndGlobal);
    };
  }, [isInteracting]);

  const handleMouseDown = (e: React.MouseEvent) => {
    if (e.button === 1 || e.button === 2 || (e.button === 0 && e.target === containerRef.current)) {
      e.preventDefault();
      setIsDragging(true);
      lastMousePos.current = { x: e.clientX, y: e.clientY };
    }
  };

  const handleWheel = (e: React.WheelEvent) => {
    e.stopPropagation();
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const mouseX = e.clientX - rect.left - rect.width / 2;
    const mouseY = e.clientY - rect.top - rect.height / 2;
    const delta = -e.deltaY * 0.001;
    const newZoom = Math.min(Math.max(0.1, zoom + delta), 8);
    const scaleRatio = newZoom / zoom;
    const mouseFromCenterX = mouseX - pan.x;
    const mouseFromCenterY = mouseY - pan.y;
    setZoom(newZoom);
    setPan({ x: mouseX - mouseFromCenterX * scaleRatio, y: mouseY - mouseFromCenterY * scaleRatio });
  };

  const handleResetZoom = (e?: React.MouseEvent) => {
    e?.stopPropagation();
    setZoom(1);
    setPan({ x: 0, y: 0 });
  };

  const calculateFullMatrix = async (currentParams: TransformParams, lines: GuideLine[]) => {
    let guidedH = IDENTITY_3X3;
    if (lines.length >= 2) {
      try {
        const res: any = await invoke('calculate_guided_perspective', { lines, width: Ow, height: Oh });
        if (res?.valid && (res?.forwardH || res?.forward_h)) {
          guidedH = res.forwardH || res.forward_h;
        }
      } catch (e) {
        console.error('Guided homography calculation failed', e);
      }
    }

    const cx = Ow / 2.0;
    const cy = Oh / 2.0;
    const ref_dim = 2000.0;
    const p_vert = (currentParams.vertical / 100000.0) * (ref_dim / Oh);
    const p_horiz = (-currentParams.horizontal / 100000.0) * (ref_dim / Ow);
    const theta = (currentParams.rotate * Math.PI) / 180.0;
    const aspect_factor =
      currentParams.aspect >= 0.0
        ? 1.0 + currentParams.aspect / 100.0
        : 1.0 / (1.0 + Math.abs(currentParams.aspect) / 100.0);
    const scale_factor = currentParams.scale / 100.0;
    const off_x = (currentParams.x_offset / 100.0) * Ow;
    const off_y = (currentParams.y_offset / 100.0) * Oh;

    const t_center = [1, 0, cx, 0, 1, cy, 0, 0, 1];
    const t_uncenter = [1, 0, -cx, 0, 1, -cy, 0, 0, 1];
    const m_perspective = [1, 0, 0, 0, 1, 0, p_horiz, p_vert, 1];
    const m_rotate = [Math.cos(theta), -Math.sin(theta), 0, Math.sin(theta), Math.cos(theta), 0, 0, 0, 1];
    const m_scale = [scale_factor * aspect_factor, 0, 0, 0, scale_factor, 0, 0, 0, 1];
    const m_offset = [1, 0, off_x, 0, 1, off_y, 0, 0, 1];

    let f = multiply3x3(t_center, m_offset);
    f = multiply3x3(f, m_perspective);
    f = multiply3x3(f, m_rotate);
    f = multiply3x3(f, m_scale);
    f = multiply3x3(f, guidedH);
    f = multiply3x3(f, t_uncenter);

    setForwardH(f);
    setInvH(invert3x3(f));
  };

  const updatePreview = useCallback(
    throttle(async (currentParams: TransformParams, lines: GuideLine[]) => {
      await calculateFullMatrix(currentParams, lines);
      try {
        const fullParams: GeometryParams = {
          ...currentParams,
          lens_distortion_amount: (currentAdjustments.lensDistortionAmount ?? 100) / SLIDER_DIVISOR,
          lens_vignette_amount: (currentAdjustments.lensVignetteAmount ?? 100) / SLIDER_DIVISOR,
          lens_tca_amount: (currentAdjustments.lensTcaAmount ?? 100) / SLIDER_DIVISOR,
          lens_dist_k1: currentAdjustments.lensDistortionParams?.k1 ?? 0,
          lens_dist_k2: currentAdjustments.lensDistortionParams?.k2 ?? 0,
          lens_dist_k3: currentAdjustments.lensDistortionParams?.k3 ?? 0,
          lens_model: currentAdjustments.lensDistortionParams?.model ?? 0,
          tca_vr: currentAdjustments.lensDistortionParams?.tca_vr ?? 1.0,
          tca_vb: currentAdjustments.lensDistortionParams?.tca_vb ?? 1.0,
          vig_k1: currentAdjustments.lensDistortionParams?.vig_k1 ?? 0,
          vig_k2: currentAdjustments.lensDistortionParams?.vig_k2 ?? 0,
          vig_k3: currentAdjustments.lensDistortionParams?.vig_k3 ?? 0,
          lens_distortion_enabled: currentAdjustments.lensDistortionEnabled ?? true,
          lens_tca_enabled: currentAdjustments.lensTcaEnabled ?? true,
          lens_vignette_enabled: currentAdjustments.lensVignetteEnabled ?? true,
          guided_lines: lines,
          guided_perspective_enabled: lines.length >= 2,
        };

        const result: string = await invoke('preview_geometry_transform', {
          params: fullParams,
          jsAdjustments: currentAdjustments,
          showLines: false,
        });
        setPreviewUrl(result);
      } catch (e) {
        console.error('Preview transform failed', e);
      }
    }, 30),
    [currentAdjustments, Ow, Oh],
  );

  useEffect(() => {
    return () => {
      updatePreview.cancel?.();
    };
  }, [updatePreview]);

  useEffect(() => {
    if (isOpen) {
      setIsMounted(true);
      const timer = setTimeout(() => setShow(true), 10);
      const initParams = {
        distortion: currentAdjustments.transformDistortion ?? 0,
        vertical: currentAdjustments.transformVertical ?? 0,
        horizontal: currentAdjustments.transformHorizontal ?? 0,
        rotate: currentAdjustments.transformRotate ?? 0,
        aspect: currentAdjustments.transformAspect ?? 0,
        scale: currentAdjustments.transformScale ?? 100,
        x_offset: currentAdjustments.transformXOffset ?? 0,
        y_offset: currentAdjustments.transformYOffset ?? 0,
      };
      setParams(initParams);

      const existingGuided = currentAdjustments.guidedPerspective;
      const initialLines = existingGuided?.lines ? structuredClone(existingGuided.lines) : [];
      setGuidedLines(initialLines);

      handleResetZoom();
      updatePreview(initParams, initialLines);
      return () => clearTimeout(timer);
    } else {
      setShow(false);
      const timer = setTimeout(() => {
        setIsMounted(false);
        setPreviewUrl(null);
        setIsApplying(false);
      }, 300);
      return () => clearTimeout(timer);
    }
  }, [isOpen, currentAdjustments]);

  const handleChange = (key: keyof typeof DEFAULT_PARAMS, value: number) => {
    const newParams = { ...params, [key]: value };
    setParams(newParams);
    updatePreview(newParams, guidedLines);
  };

  const handleApply = () => {
    setIsApplying(true);
    try {
      onApply({
        transformDistortion: params.distortion,
        transformVertical: params.vertical,
        transformHorizontal: params.horizontal,
        transformRotate: params.rotate,
        transformAspect: params.aspect,
        transformScale: params.scale,
        transformXOffset: params.x_offset,
        transformYOffset: params.y_offset,
        guidedPerspective: {
          enabled: guidedLines.length >= 2,
          lines: guidedLines,
          autoCrop: true,
        },
      });
      onClose();
    } catch (e) {
      console.error('Failed to apply transform', e);
      setIsApplying(false);
    }
  };

  const handleReset = () => {
    setParams(DEFAULT_PARAMS);
    setGuidedLines([]);
    setSelectedGuideId(null);
    updatePreview(DEFAULT_PARAMS, []);
  };

  const toggleCompare = async (active: boolean) => {
    setIsCompareActive(active);
    if (active) {
      const fullParams: GeometryParams = {
        ...DEFAULT_PARAMS,
        lens_distortion_amount: (currentAdjustments.lensDistortionAmount ?? 100) / SLIDER_DIVISOR,
        lens_vignette_amount: (currentAdjustments.lensVignetteAmount ?? 100) / SLIDER_DIVISOR,
        lens_tca_amount: (currentAdjustments.lensTcaAmount ?? 100) / SLIDER_DIVISOR,
        lens_dist_k1: currentAdjustments.lensDistortionParams?.k1 ?? 0,
        lens_dist_k2: currentAdjustments.lensDistortionParams?.k2 ?? 0,
        lens_dist_k3: currentAdjustments.lensDistortionParams?.k3 ?? 0,
        lens_model: currentAdjustments.lensDistortionParams?.model ?? 0,
        tca_vr: currentAdjustments.lensDistortionParams?.tca_vr ?? 1.0,
        tca_vb: currentAdjustments.lensDistortionParams?.tca_vb ?? 1.0,
        vig_k1: currentAdjustments.lensDistortionParams?.vig_k1 ?? 0,
        vig_k2: currentAdjustments.lensDistortionParams?.vig_k2 ?? 0,
        vig_k3: currentAdjustments.lensDistortionParams?.vig_k3 ?? 0,
        lens_distortion_enabled: currentAdjustments.lensDistortionEnabled ?? true,
        lens_tca_enabled: currentAdjustments.lensTcaEnabled ?? true,
        lens_vignette_enabled: currentAdjustments.lensVignetteEnabled ?? true,
        guided_lines: [],
        guided_perspective_enabled: false,
      };
      const result: string = await invoke('preview_geometry_transform', {
        params: fullParams,
        jsAdjustments: currentAdjustments,
        showLines: false,
      });
      setPreviewUrl(result);
    } else {
      updatePreview(params, guidedLines);
    }
  };

  const mapUvToScreen = (uv: Coord) => {
    if (renderDims.width <= 0 || renderDims.height <= 0) return { x: 0, y: 0 };
    const ox = uv.x * Ow;
    const oy = uv.y * Oh;
    const warped = project3x3(forwardH, ox, oy);
    let px = warped.x;
    let py = warped.y;

    const oriented = orientPoint(px, py, Ow, Oh, orientationSteps);
    px = oriented.x;
    py = oriented.y;
    if (flipH) px = Dw - px;
    if (flipV) py = Dh - py;

    return { x: (px / Dw) * renderDims.width, y: (py / Dh) * renderDims.height };
  };

  const mapScreenToUv = (stageX: number, stageY: number): Coord => {
    if (renderDims.width <= 0 || renderDims.height <= 0) return { x: 0, y: 0 };
    let px = (stageX / renderDims.width) * Dw;
    let py = (stageY / renderDims.height) * Dh;
    if (flipH) px = Dw - px;
    if (flipV) py = Dh - py;

    const unoriented = unorientPoint(px, py, Dw, Dh, orientationSteps);
    px = unoriented.x;
    py = unoriented.y;
    const orig = project3x3(invH, px, py);

    return {
      x: Math.max(0, Math.min(1, orig.x / Ow)),
      y: Math.max(0, Math.min(1, orig.y / Oh)),
    };
  };

  const handleStageMouseDown = (e: any) => {
    if (e.evt.button === 1 || e.evt.button === 2) {
      e.evt.preventDefault();
      setIsDragging(true);
      lastMousePos.current = { x: e.evt.clientX, y: e.evt.clientY };
      return;
    }
    const stage = e.target.getStage();
    if (e.target !== stage) return;
    const pos = stage.getPointerPosition();
    if (!pos || renderDims.width <= 0) return;

    setSelectedGuideId(null);
    const uv = mapScreenToUv(pos.x, pos.y);
    setDraftLine({ p1: uv, p2: uv });
  };

  const handleStageMouseMove = (e: any) => {
    if (!draftLine) return;
    const stage = e.target.getStage();
    const pos = stage.getPointerPosition();
    if (!pos) return;
    const uv = mapScreenToUv(pos.x, pos.y);
    setDraftLine({ p1: draftLine.p1, p2: uv });
  };

  const handleStageMouseUp = () => {
    if (!draftLine) return;
    const { p1, p2 } = draftLine;
    setDraftLine(null);

    const dx = (p2.x - p1.x) * Ow;
    const dy = (p2.y - p1.y) * Oh;
    if (Math.hypot(dx, dy) < 15) return;

    const tan35 = Math.tan((35 * Math.PI) / 180);
    const isVert = Math.abs(dx) <= Math.abs(dy) * tan35;
    const isHoriz = Math.abs(dy) <= Math.abs(dx) * tan35;

    if (!isVert && !isHoriz) {
      toast.error(t('editor.guided.toast.angleRejected'));
      return;
    }

    const type: GuideOrientation = isVert ? 'vertical' : 'horizontal';
    if (guidedLines.filter((l) => l.type === type).length >= 2) {
      toast.error(t('editor.guided.toast.maxLines'));
      return;
    }

    const newLine: GuideLine = { id: uuidv4(), type, p1, p2 };
    const next = [...guidedLines, newLine];
    setGuidedLines(next);
    setSelectedGuideId(newLine.id);
    updatePreview(params, next);
  };

  const removeLine = (lineId: string) => {
    const next = guidedLines.filter((l) => l.id !== lineId);
    setGuidedLines(next);
    if (selectedGuideId === lineId) setSelectedGuideId(null);
    updatePreview(params, next);
  };

  const renderControls = () => (
    <div className="modal-adjustments-pane w-80 shrink-0 bg-bg-secondary flex flex-col border-l border-surface h-full z-10">
      <div className="p-4 flex justify-between items-center shrink-0 border-b border-surface">
        <Text variant={TextVariants.title}>{t('modals.transform.title')}</Text>
        <button
          onClick={handleReset}
          data-tooltip={t('modals.transform.resetTooltip')}
          className="p-2 rounded-full hover:bg-surface transition-colors"
        >
          <RotateCcw size={18} />
        </button>
      </div>

      <div className="grow overflow-y-auto p-4 flex flex-col gap-6" onPointerDownCapture={() => setIsInteracting(true)}>
        <div className="flex flex-col gap-4">
          <Text variant={TextVariants.heading}>{t('modals.transform.guided')}</Text>
          <Text variant={TextVariants.body} color={TextColors.secondary}>
            {t('editor.guided.hint')}
          </Text>

          <div className="p-3 bg-surface rounded-lg border border-surface flex flex-col gap-2">
            <div className="flex justify-between items-center text-xs font-medium">
              <span>{t('editor.guided.linesStatus')}</span>
              <span className={clsx(guidedLines.length >= 2 ? 'text-accent' : 'text-text-secondary')}>
                {guidedLines.length} / 4
              </span>
            </div>
            {guidedLines.length > 0 && (
              <div className="flex flex-col gap-1 mt-1">
                {guidedLines.map((line, idx) => {
                  const isSelected = selectedGuideId === line.id;

                  return (
                    <div
                      key={line.id}
                      onClick={() => setSelectedGuideId(line.id)}
                      className={clsx(
                        'flex items-center gap-2 p-2 rounded-md transition-colors group cursor-pointer',
                        isSelected ? 'bg-card-active' : 'hover:bg-card-active/50',
                      )}
                    >
                      <Text
                        as="div"
                        color={isSelected ? TextColors.primary : TextColors.secondary}
                        className="p-0.5 rounded transition-colors shrink-0 flex items-center justify-center"
                      >
                        <Minus size={16} />
                      </Text>

                      <div className="flex-1 min-w-0">
                        <Text
                          color={TextColors.primary}
                          weight={TextWeights.medium}
                          className="truncate select-none text-xs"
                        >
                          <span className="capitalize">{line.type} Guide</span> #{idx + 1}
                        </Text>
                      </div>

                      <div className="flex items-center opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          className="p-1 hover:text-red-500 text-text-secondary transition-colors"
                          onClick={(e) => {
                            e.stopPropagation();
                            removeLine(line.id);
                          }}
                        >
                          <Trash2 size={16} />
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>

        <div className="h-px bg-surface w-full" />

        <div className="flex flex-col gap-3">
          <Text variant={TextVariants.heading}>{t('modals.transform.manual')}</Text>

          <Slider
            label={t('modals.transform.distortion')}
            value={params.distortion}
            min={-100}
            max={100}
            defaultValue={0}
            step={1}
            onChange={(e) => handleChange('distortion', Number(e.target.value))}
          />

          <Slider
            label={t('modals.transform.vertical')}
            value={params.vertical}
            min={-100}
            max={100}
            defaultValue={0}
            step={1}
            onChange={(e) => handleChange('vertical', Number(e.target.value))}
          />

          <Slider
            label={t('modals.transform.horizontal')}
            value={params.horizontal}
            min={-100}
            max={100}
            defaultValue={0}
            step={1}
            onChange={(e) => handleChange('horizontal', Number(e.target.value))}
          />

          <Slider
            label={t('modals.transform.rotate')}
            value={params.rotate}
            min={-45}
            max={45}
            step={0.1}
            defaultValue={0}
            onChange={(e) => handleChange('rotate', Number(e.target.value))}
          />

          <Slider
            label={t('modals.transform.aspect')}
            value={params.aspect}
            min={-100}
            max={100}
            defaultValue={0}
            step={1}
            onChange={(e) => handleChange('aspect', Number(e.target.value))}
          />

          <Slider
            label={t('modals.transform.scale')}
            value={params.scale}
            min={50}
            max={150}
            defaultValue={100}
            step={1}
            onChange={(e) => handleChange('scale', Number(e.target.value))}
          />

          <Slider
            label={t('modals.transform.xAxis')}
            value={params.x_offset}
            min={-100}
            max={100}
            defaultValue={0}
            step={1}
            onChange={(e) => handleChange('x_offset', Number(e.target.value))}
          />

          <Slider
            label={t('modals.transform.yAxis')}
            value={params.y_offset}
            min={-100}
            max={100}
            defaultValue={0}
            step={1}
            onChange={(e) => handleChange('y_offset', Number(e.target.value))}
          />
        </div>

        <div className="mt-auto">
          {currentAdjustments.masks && currentAdjustments.masks.length > 0 && (
            <Text
              as="div"
              variant={TextVariants.small}
              className="p-3 bg-surface rounded-md border border-surface flex items-center gap-3"
            >
              <Info size={16} className="shrink-0" />
              <p className="leading-relaxed">{t('modals.transform.maskWarning')}</p>
            </Text>
          )}
        </div>
      </div>
    </div>
  );

  const imageTransformStyle = {
    transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`,
    transition: isDragging ? 'none' : 'transform 0.1s ease-out',
    transformOrigin: 'center center',
  };

  const renderContent = () => (
    <div className="modal-preview-adjustments flex flex-row h-full w-full overflow-hidden">
      <div className="modal-preview-pane grow flex flex-col relative min-h-0 bg-[#0f0f0f] overflow-hidden">
        <div
          ref={containerRef}
          onContextMenu={(e) => e.preventDefault()}
          className={clsx(
            'flex-1 relative overflow-hidden select-none',
            isDragging ? 'cursor-grabbing' : 'cursor-crosshair',
          )}
          onMouseDown={handleMouseDown}
          onWheel={handleWheel}
        >
          <div
            className="absolute inset-0 opacity-20 pointer-events-none"
            style={{ backgroundImage: 'radial-gradient(#444 1px, transparent 1px)', backgroundSize: '24px 24px' }}
          />

          {previewUrl && (
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
              <div className="origin-center" style={imageTransformStyle}>
                <div className="relative inline-block shadow-2xl">
                  <img
                    ref={imgRef}
                    src={previewUrl}
                    className="block object-contain"
                    style={{ maxWidth: '100%', maxHeight: '100%', width: 'auto', height: 'auto' }}
                    alt="Transform Preview"
                    draggable={false}
                    onLoad={measureImage}
                  />

                  {!isCompareActive && (
                    <CustomGrid ruleOfThirdsVisible={showGrid} denseVisible={showGrid && isInteracting} />
                  )}

                  {renderDims.width > 0 && renderDims.height > 0 && !isCompareActive && (
                    <div
                      className={clsx(
                        'absolute inset-0 z-20 pointer-events-auto',
                        isDragging ? 'cursor-grabbing' : 'cursor-crosshair',
                      )}
                    >
                      <Stage
                        width={renderDims.width}
                        height={renderDims.height}
                        onMouseDown={handleStageMouseDown}
                        onMouseMove={handleStageMouseMove}
                        onMouseUp={handleStageMouseUp}
                      >
                        <Layer>
                          {guidedLines.map((line) => {
                            const sc1 = mapUvToScreen(line.p1);
                            const sc2 = mapUvToScreen(line.p2);
                            const isSelected = selectedGuideId === line.id;

                            return (
                              <Fragment key={line.id}>
                                <Line
                                  points={[sc1.x, sc1.y, sc2.x, sc2.y]}
                                  stroke={isSelected ? '#3b82f6' : '#ffffff'}
                                  strokeWidth={isSelected ? 2.5 : 1.5}
                                  dash={isSelected ? undefined : [6, 4]}
                                  hitStrokeWidth={14}
                                  onClick={() => setSelectedGuideId(line.id)}
                                />
                                <Circle
                                  x={sc1.x}
                                  y={sc1.y}
                                  radius={6}
                                  fill="#ffffff"
                                  stroke="#3b82f6"
                                  strokeWidth={2}
                                  draggable
                                  onDragMove={(e) => {
                                    const next = guidedLines.map((l) =>
                                      l.id === line.id ? { ...l, p1: mapScreenToUv(e.target.x(), e.target.y()) } : l,
                                    );
                                    setGuidedLines(next);
                                  }}
                                  onDragEnd={() => updatePreview(params, guidedLines)}
                                />
                                <Circle
                                  x={sc2.x}
                                  y={sc2.y}
                                  radius={6}
                                  fill="#ffffff"
                                  stroke="#3b82f6"
                                  strokeWidth={2}
                                  draggable
                                  onDragMove={(e) => {
                                    const next = guidedLines.map((l) =>
                                      l.id === line.id ? { ...l, p2: mapScreenToUv(e.target.x(), e.target.y()) } : l,
                                    );
                                    setGuidedLines(next);
                                  }}
                                  onDragEnd={() => updatePreview(params, guidedLines)}
                                />
                              </Fragment>
                            );
                          })}

                          {draftLine && (
                            <Line
                              points={[
                                mapUvToScreen(draftLine.p1).x,
                                mapUvToScreen(draftLine.p1).y,
                                mapUvToScreen(draftLine.p2).x,
                                mapUvToScreen(draftLine.p2).y,
                              ]}
                              stroke="#3b82f6"
                              strokeWidth={1.5}
                              dash={[4, 4]}
                            />
                          )}
                        </Layer>
                      </Stage>
                    </div>
                  )}

                  {isCompareActive && (
                    <Text
                      as="div"
                      variant={TextVariants.small}
                      color={TextColors.button}
                      className="absolute top-4 left-4 bg-accent px-2 py-1 rounded-sm shadow-lg z-30 pointer-events-none"
                    >
                      {t('modals.transform.original')}
                    </Text>
                  )}
                </div>
              </div>
            </div>
          )}

          <div
            className="absolute bottom-6 left-1/2 -translate-x-1/2 flex items-center gap-1 bg-black/70 backdrop-blur-md p-1.5 rounded-full border border-white/10 shadow-xl z-30 pointer-events-auto"
            onMouseDown={(e) => e.stopPropagation()}
          >
            <button
              onClick={() => setShowGrid(!showGrid)}
              className={clsx(
                'p-2 rounded-full transition-colors',
                showGrid ? 'bg-white/20 text-white' : 'text-white/60 hover:bg-white/10 hover:text-white',
              )}
              data-tooltip={t('modals.transform.toggleGridTooltip')}
            >
              <Grid3X3 size={18} />
            </button>
            <div className="w-px h-5 bg-white/20 mx-1" />

            <button
              onClick={() => setZoom((z) => Math.max(0.1, z - 0.25))}
              className="p-2 text-white/60 hover:bg-white/10 hover:text-white rounded-full transition-colors"
              data-tooltip={t('modals.transform.zoomOutTooltip')}
            >
              <ZoomOut size={18} />
            </button>

            <span className="text-xs font-mono text-white/90 w-12 text-center select-none pointer-events-none">
              {Math.round(zoom * 100)}%
            </span>

            <button
              onClick={() => setZoom((z) => Math.min(8, z + 0.25))}
              className="p-2 text-white/60 hover:bg-white/10 hover:text-white rounded-full transition-colors"
              data-tooltip={t('modals.transform.zoomInTooltip')}
            >
              <ZoomIn size={18} />
            </button>

            <button
              onClick={handleResetZoom}
              className="p-2 text-white/60 hover:bg-white/10 hover:text-white rounded-full transition-colors"
              data-tooltip={t('modals.transform.resetZoomTooltip')}
            >
              <Maximize size={16} />
            </button>

            <div className="w-px h-5 bg-white/20 mx-1" />

            <button
              onMouseDown={() => toggleCompare(true)}
              onMouseUp={() => toggleCompare(false)}
              onMouseLeave={() => toggleCompare(false)}
              className={clsx(
                'p-2 rounded-full transition-colors select-none',
                isCompareActive ? 'bg-accent text-button-text' : 'text-white/60 hover:bg-white/10 hover:text-white',
              )}
              data-tooltip={t('modals.transform.compareTooltip')}
            >
              {isCompareActive ? <Eye size={18} /> : <EyeOff size={18} />}
            </button>
          </div>
        </div>
      </div>
      {renderControls()}
    </div>
  );

  if (!isMounted) return null;

  return (
    <div
      className={`fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs transition-opacity duration-300 ${
        show ? 'opacity-100' : 'opacity-0'
      }`}
      onMouseDown={onClose}
    >
      <AnimatePresence>
        {show && (
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.95, opacity: 0 }}
            transition={{ duration: 0.2, ease: 'easeOut' }}
            className="bg-surface rounded-lg shadow-xl w-full max-w-6xl h-[90vh] flex flex-col overflow-hidden"
            onMouseDown={(e) => e.stopPropagation()}
          >
            <div className="grow min-h-0 overflow-hidden">{renderContent()}</div>
            <div className="shrink-0 p-4 flex justify-end gap-3 border-t border-surface bg-bg-secondary z-20">
              <button
                onClick={onClose}
                className="px-4 py-2 rounded-md text-text-secondary hover:bg-surface transition-colors"
              >
                {t('modals.transform.cancel')}
              </button>
              <Button onClick={handleApply} disabled={isApplying || !previewUrl}>
                <Check className="mr-2" size={16} />
                {t('modals.transform.apply')}
              </Button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
