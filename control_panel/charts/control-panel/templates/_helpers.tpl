{{/*
Common labels
*/}}
{{- define "control-panel.labels" -}}
app.kubernetes.io/name: control-panel
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
{{- end -}}

{{/*
Selector labels
*/}}
{{- define "control-panel.selectorLabels" -}}
app.kubernetes.io/name: control-panel
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/*
AES_KEY: 32 random bytes base64. Pinned if .Values.secrets.aesKey set.
*/}}
{{- define "control-panel.aesKey" -}}
{{- if .Values.secrets.aesKey -}}
{{- .Values.secrets.aesKey -}}
{{- else -}}
{{- randAlphaNum 44 | b64enc -}}
{{- end -}}
{{- end -}}

{{/*
JWT_SECRET: random base64. Pinned if .Values.secrets.jwtSecret set.
*/}}
{{- define "control-panel.jwtSecret" -}}
{{- if .Values.secrets.jwtSecret -}}
{{- .Values.secrets.jwtSecret -}}
{{- else -}}
{{- randAlphaNum 44 | b64enc -}}
{{- end -}}
{{- end -}}

{{/*
ADMIN_INIT_PASSWORD: plaintext, base64-encoded for the Secret data field.
Pinned if .Values.secrets.adminPassword set, else auto-generated.
*/}}
{{- define "control-panel.adminPassword" -}}
{{- if .Values.secrets.adminPassword -}}
{{- .Values.secrets.adminPassword | b64enc -}}
{{- else -}}
{{- randAlphaNum 16 | b64enc -}}
{{- end -}}
{{- end -}}
