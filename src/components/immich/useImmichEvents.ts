import { useEffect, useRef } from 'react';
import { listen } from '@tauri-apps/api/event';
import { toast } from 'react-toastify';
import { useTranslation } from 'react-i18next';
import { useLibraryStore } from '../../store/useLibraryStore';
import { ImmichSyncStatus } from './immichApi';
import { useImmichStore } from './useImmichStore';

interface DownloadEvent {
  path: string;
  state: 'started' | 'done' | 'error';
  error?: string;
}

interface UploadEvent {
  fileName: string;
  state: 'done' | 'error';
  error?: string;
}

interface ConflictEvent {
  path: string;
  fileName: string;
}

const REFRESH_DELAY_MS = 1500;

export function useImmichEvents(refreshLibrary: () => void) {
  const { t } = useTranslation();
  const refreshRef = useRef(refreshLibrary);
  refreshRef.current = refreshLibrary;
  const refreshTimer = useRef<ReturnType<typeof setTimeout>>(undefined);
  const uploaded = useRef(0);

  useEffect(() => {
    const unlisteners = [
      listen<DownloadEvent>('immich-download', ({ payload }) => {
        if (payload.state === 'done') {
          useLibraryStore.getState().setLibrary((state) => ({
            imageList: state.imageList.map((image) =>
              image.path === payload.path ? { ...image, is_cloud_placeholder: false } : image,
            ),
          }));
        } else if (payload.state === 'error') {
          toast.error(t('immich.toasts.downloadFailed', { error: payload.error }));
        }
      }),
      listen<ImmichSyncStatus>('immich-sync', ({ payload }) => {
        const previous = useImmichStore.getState().syncStatus;
        if (payload.offline && !previous.offline) {
          toast.warning(t('immich.toasts.offline'));
        } else if (previous.offline && !payload.offline && payload.pending === 0) {
          toast.success(t('immich.toasts.backOnline'));
        }
        useImmichStore.getState().setSyncStatus(payload);
      }),
      listen<UploadEvent>('immich-upload', ({ payload }) => {
        if (payload.state === 'done') {
          uploaded.current += 1;
        } else {
          toast.error(t('immich.toasts.uploadFailed', { fileName: payload.fileName, error: payload.error }));
        }
      }),
      listen('immich-library-changed', () => {
        clearTimeout(refreshTimer.current);
        refreshTimer.current = setTimeout(() => {
          if (uploaded.current > 0) {
            toast.success(t('immich.toasts.uploaded', { number: uploaded.current }));
            uploaded.current = 0;
          }
          useImmichStore.getState().loadAlbums();
          refreshRef.current();
        }, REFRESH_DELAY_MS);
      }),
      listen<{ error: string }>('immich-trash', ({ payload }) => {
        toast.error(t('immich.toasts.trashFailed', { error: payload.error }));
      }),
      listen<ConflictEvent>('immich-edits-conflict', ({ payload }) => {
        toast.info(t('immich.toasts.editsConflict', { fileName: payload.fileName }));
        refreshRef.current();
      }),
    ];

    return () => {
      clearTimeout(refreshTimer.current);
      unlisteners.forEach((unlisten) => unlisten.then((fn) => fn()));
    };
  }, [t]);
}
