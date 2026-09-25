package db

import (
	"context"
	"database/sql"
	"errors"
	"strings"
	"time"
)

func (s *Store) UpsertNotebookMetadata(ctx context.Context, metadata NotebookMetadata) error {
	now := time.Now().UTC()
	_, err := s.db.ExecContext(ctx, `
INSERT INTO notebook_metadata
  (stable_key, key_kind, namespace, workspace_id, project_id, last_pod_uid, owner_name, note, updated_by, created_at, updated_at)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(stable_key) DO UPDATE SET
  key_kind=excluded.key_kind,
  namespace=excluded.namespace,
  workspace_id=excluded.workspace_id,
  project_id=excluded.project_id,
  last_pod_uid=excluded.last_pod_uid,
  owner_name=excluded.owner_name,
  note=excluded.note,
  updated_by=excluded.updated_by,
  updated_at=excluded.updated_at`,
		metadata.StableKey, metadata.KeyKind, metadata.Namespace, metadata.WorkspaceID, metadata.ProjectID,
		metadata.LastPodUID, metadata.OwnerName, metadata.Note, metadata.UpdatedBy, now, now)
	return err
}

func (s *Store) GetNotebookMetadata(ctx context.Context, stableKey string) (*NotebookMetadata, error) {
	var metadata NotebookMetadata
	err := scanNotebookMetadata(s.db.QueryRowContext(ctx, `
SELECT stable_key, key_kind, namespace, workspace_id, project_id, last_pod_uid,
       owner_name, note, updated_by, created_at, updated_at
FROM notebook_metadata WHERE stable_key=?`, stableKey), &metadata)
	if errors.Is(err, sql.ErrNoRows) {
		return nil, ErrNotFound
	}
	if err != nil {
		return nil, err
	}
	return &metadata, nil
}

func (s *Store) GetNotebookMetadataByKeys(ctx context.Context, stableKeys []string) (map[string]NotebookMetadata, error) {
	out := make(map[string]NotebookMetadata)
	if len(stableKeys) == 0 {
		return out, nil
	}
	placeholders := strings.TrimSuffix(strings.Repeat("?,", len(stableKeys)), ",")
	args := make([]any, len(stableKeys))
	for i, key := range stableKeys {
		args[i] = key
	}
	rows, err := s.db.QueryContext(ctx, `
SELECT stable_key, key_kind, namespace, workspace_id, project_id, last_pod_uid,
       owner_name, note, updated_by, created_at, updated_at
FROM notebook_metadata WHERE stable_key IN (`+placeholders+")", args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	for rows.Next() {
		var metadata NotebookMetadata
		if err := rows.Scan(&metadata.StableKey, &metadata.KeyKind, &metadata.Namespace,
			&metadata.WorkspaceID, &metadata.ProjectID, &metadata.LastPodUID, &metadata.OwnerName,
			&metadata.Note, &metadata.UpdatedBy, &metadata.CreatedAt, &metadata.UpdatedAt); err != nil {
			return nil, err
		}
		out[metadata.StableKey] = metadata
	}
	return out, rows.Err()
}

func (s *Store) DeleteNotebookMetadata(ctx context.Context, stableKey string) error {
	_, err := s.db.ExecContext(ctx, "DELETE FROM notebook_metadata WHERE stable_key=?", stableKey)
	return err
}

type rowScanner interface {
	Scan(dest ...any) error
}

func scanNotebookMetadata(row rowScanner, metadata *NotebookMetadata) error {
	return row.Scan(&metadata.StableKey, &metadata.KeyKind, &metadata.Namespace,
		&metadata.WorkspaceID, &metadata.ProjectID, &metadata.LastPodUID, &metadata.OwnerName,
		&metadata.Note, &metadata.UpdatedBy, &metadata.CreatedAt, &metadata.UpdatedAt)
}
