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

interface ConflictEvent {
  path: string;
  fileName: string;
}

export function useImmichEvents(refreshLibrary: () => void) {
  const { t } = useTranslation();
  const refreshRef = useRef(refreshLibrary);
  refreshRef.current = refreshLibrary;

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
      listen<ConflictEvent>('immich-edits-conflict', ({ payload }) => {
        toast.info(t('immich.toasts.editsConflict', { fileName: payload.fileName }));
        refreshRef.current();
      }),
    ];

    return () => {
      unlisteners.forEach((unlisten) => unlisten.then((fn) => fn()));
    };
  }, [t]);
}
