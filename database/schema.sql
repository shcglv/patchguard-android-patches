-- PatchGuard Android Patches — canonical SQLite schema (latest).
-- Local working database only. Public source of truth is Git (catalog/, audits/).
-- Apply migrations in database/migrations/ in order. This file must equal the
-- cumulative result of the migrations; tests enforce that.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_migrations (
    version     INTEGER PRIMARY KEY,
    applied_at  TEXT NOT NULL,
    checksum    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS applications (
    id                 INTEGER PRIMARY KEY,
    slug               TEXT NOT NULL UNIQUE,
    name               TEXT NOT NULL,
    package_name       TEXT NOT NULL UNIQUE,
    developer          TEXT,
    category           TEXT NOT NULL,
    security_class     TEXT NOT NULL DEFAULT 'NORMAL'
                       CHECK (security_class IN ('NORMAL', 'CRITICAL')),
    supported_versions TEXT NOT NULL DEFAULT '[]',
    official_website   TEXT,
    notes              TEXT,
    created_at         TEXT NOT NULL,
    updated_at         TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sources (
    id                  INTEGER PRIMARY KEY,
    slug                TEXT NOT NULL UNIQUE,
    name                TEXT NOT NULL,
    repository_url      TEXT NOT NULL UNIQUE,
    host                TEXT NOT NULL CHECK (host IN ('github.com', 'gitlab.com')),
    owner               TEXT NOT NULL,
    source_type         TEXT NOT NULL
                        CHECK (source_type IN ('github_repository', 'gitlab_repository')),
    license             TEXT NOT NULL,
    license_evidence    TEXT,
    trust_level         TEXT NOT NULL
                        CHECK (trust_level IN ('OFFICIAL', 'MAINTAINED', 'COMMUNITY', 'UNTRUSTED')),
    tracked_branch      TEXT NOT NULL,
    last_checked_commit TEXT,
    latest_release      TEXT,
    last_checked_at     TEXT,
    repository_status   TEXT NOT NULL DEFAULT 'UNKNOWN'
                        CHECK (repository_status IN ('ACTIVE', 'ARCHIVED', 'RENAMED', 'UNAVAILABLE', 'UNKNOWN')),
    aliases             TEXT NOT NULL DEFAULT '[]',
    notes               TEXT,
    created_at          TEXT NOT NULL,
    updated_at          TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS source_revisions (
    id                   INTEGER PRIMARY KEY,
    source_id            INTEGER NOT NULL REFERENCES sources(id) ON DELETE RESTRICT,
    commit_sha           TEXT NOT NULL,
    release_tag          TEXT,
    release_date         TEXT,
    source_sha256        TEXT NOT NULL,
    file_manifest_sha256 TEXT NOT NULL,
    archive_sha256       TEXT,
    change_summary       TEXT,
    checked_at           TEXT NOT NULL,
    UNIQUE (source_id, commit_sha)
);

CREATE TABLE IF NOT EXISTS patches (
    id                              INTEGER PRIMARY KEY,
    slug                            TEXT NOT NULL UNIQUE,
    name                            TEXT NOT NULL,
    application_id                  INTEGER NOT NULL REFERENCES applications(id) ON DELETE RESTRICT,
    source_id                       INTEGER NOT NULL REFERENCES sources(id) ON DELETE RESTRICT,
    source_commit                   TEXT NOT NULL,
    source_sha256                   TEXT NOT NULL,
    original_author                 TEXT,
    description                     TEXT,
    functionality                   TEXT,
    category                        TEXT NOT NULL
                                    CHECK (category IN ('UI', 'ADVERTISING', 'PRIVACY', 'FUNCTIONALITY', 'NETWORK', 'SECURITY_SENSITIVE')),
    version                         TEXT,
    supported_app_versions          TEXT NOT NULL DEFAULT '[]',
    required_patcher_version        TEXT,
    dependencies                    TEXT NOT NULL DEFAULT '[]',
    modified_components             TEXT NOT NULL DEFAULT '[]',
    permissions                     TEXT NOT NULL DEFAULT '[]',
    network_activity                TEXT NOT NULL DEFAULT '[]',
    audit_status                    TEXT NOT NULL DEFAULT 'DISCOVERED'
                                    CHECK (audit_status IN ('DISCOVERED', 'PENDING', 'STATIC_AUDITING', 'STATICALLY_REVIEWED', 'UNVERIFIED', 'REJECTED', 'BLOCKED', 'UPDATE_AVAILABLE', 'OUTDATED')),
    distribution_status             TEXT NOT NULL DEFAULT 'NOT_ELIGIBLE'
                                    CHECK (distribution_status IN ('NOT_ELIGIBLE', 'CANDIDATE', 'APPROVED', 'BLOCKED')),
    audit_scope                     TEXT NOT NULL DEFAULT 'SOURCE_CODE_ONLY'
                                    CHECK (audit_scope = 'SOURCE_CODE_ONLY'),
    runtime_tested                  INTEGER NOT NULL DEFAULT 0 CHECK (runtime_tested = 0),
    apk_tested                      INTEGER NOT NULL DEFAULT 0 CHECK (apk_tested = 0),
    compatibility_runtime_verified  INTEGER NOT NULL DEFAULT 0 CHECK (compatibility_runtime_verified = 0),
    risk_score                      INTEGER CHECK (risk_score BETWEEN 0 AND 100),
    confidence_level                TEXT CHECK (confidence_level IN ('LOW', 'MEDIUM')),
    audit_tools                     TEXT NOT NULL DEFAULT '[]',
    audit_limitations               TEXT NOT NULL DEFAULT '[]',
    last_audited_at                 TEXT,
    last_updated_at                 TEXT,
    notes                           TEXT
);

CREATE TABLE IF NOT EXISTS audits (
    id                             INTEGER PRIMARY KEY,
    audit_id                       TEXT NOT NULL UNIQUE,
    patch_id                       INTEGER NOT NULL REFERENCES patches(id) ON DELETE RESTRICT,
    source_commit                  TEXT NOT NULL,
    source_sha256                  TEXT NOT NULL,
    audit_date                     TEXT NOT NULL,
    audit_type                     TEXT NOT NULL
                                   CHECK (audit_type IN ('INITIAL', 'RE_AUDIT', 'UPDATE_IMPACT', 'LICENSE_REVIEW')),
    auditor                        TEXT NOT NULL,
    audit_scope                    TEXT NOT NULL DEFAULT 'SOURCE_CODE_ONLY'
                                    CHECK (audit_scope = 'SOURCE_CODE_ONLY'),
    runtime_tested                 INTEGER NOT NULL DEFAULT 0 CHECK (runtime_tested = 0),
    apk_tested                     INTEGER NOT NULL DEFAULT 0 CHECK (apk_tested = 0),
    compatibility_runtime_verified INTEGER NOT NULL DEFAULT 0 CHECK (compatibility_runtime_verified = 0),
    findings_json                  TEXT NOT NULL DEFAULT '[]',
    severity                       TEXT,
    evidence                       TEXT,
    audit_tools                    TEXT NOT NULL DEFAULT '[]',
    coverage                       TEXT NOT NULL DEFAULT '{}',
    limitations                    TEXT NOT NULL DEFAULT '[]',
    tested_versions                TEXT NOT NULL DEFAULT '[]',
    report_path                    TEXT NOT NULL,
    audit_result                   TEXT NOT NULL
                                   CHECK (audit_result IN ('STATICALLY_REVIEWED', 'UNVERIFIED', 'REJECTED', 'BLOCKED')),
    risk_score                     INTEGER CHECK (risk_score BETWEEN 0 AND 100),
    confidence_level               TEXT CHECK (confidence_level IN ('LOW', 'MEDIUM'))
);

CREATE TABLE IF NOT EXISTS findings (
    id             INTEGER PRIMARY KEY,
    finding_id     TEXT NOT NULL UNIQUE,
    audit_id       INTEGER NOT NULL REFERENCES audits(id) ON DELETE RESTRICT,
    severity       TEXT NOT NULL CHECK (severity IN ('INFO', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    category       TEXT NOT NULL,
    description    TEXT NOT NULL,
    file_path      TEXT,
    line_reference TEXT,
    evidence       TEXT,
    remediation    TEXT,
    status         TEXT NOT NULL DEFAULT 'OPEN'
                   CHECK (status IN ('OPEN', 'ACCEPTED', 'FIXED', 'FALSE_POSITIVE', 'NOT_APPLICABLE'))
);

CREATE TABLE IF NOT EXISTS dependencies (
    id                   INTEGER PRIMARY KEY,
    patch_id             INTEGER NOT NULL REFERENCES patches(id) ON DELETE RESTRICT,
    package_name         TEXT NOT NULL,
    version              TEXT,
    source               TEXT,
    license              TEXT,
    known_vulnerabilities TEXT NOT NULL DEFAULT '[]',
    last_checked         TEXT,
    UNIQUE (patch_id, package_name, version)
);

CREATE TABLE IF NOT EXISTS compatibility_assessments (
    id             INTEGER PRIMARY KEY,
    patch_id       INTEGER NOT NULL REFERENCES patches(id) ON DELETE RESTRICT,
    app_version    TEXT,
    version_code   INTEGER,
    basis          TEXT NOT NULL
                   CHECK (basis IN ('DECLARED', 'STATICALLY_ASSESSED', 'NOT_RUNTIME_TESTED')),
    evidence       TEXT,
    notes          TEXT,
    assessed_at    TEXT
);

CREATE TABLE IF NOT EXISTS attribution (
    id                     INTEGER PRIMARY KEY,
    patch_id               INTEGER NOT NULL UNIQUE REFERENCES patches(id) ON DELETE RESTRICT,
    original_author        TEXT,
    original_repository    TEXT,
    source_commit          TEXT,
    source_license         TEXT,
    inspiration_source     TEXT,
    related_issue          TEXT,
    related_pull_request   TEXT,
    upstream_documentation TEXT,
    reused_files           TEXT NOT NULL DEFAULT '[]',
    modifications          TEXT,
    attribution_text       TEXT
);

CREATE TABLE IF NOT EXISTS update_checks (
    id              INTEGER PRIMARY KEY,
    source_id       INTEGER NOT NULL REFERENCES sources(id) ON DELETE RESTRICT,
    previous_commit TEXT,
    current_commit  TEXT,
    changed_files   TEXT NOT NULL DEFAULT '[]',
    detected_changes TEXT NOT NULL DEFAULT '{}',
    audit_required  INTEGER NOT NULL DEFAULT 0 CHECK (audit_required IN (0, 1)),
    result          TEXT NOT NULL
                    CHECK (result IN ('NO_CHANGE', 'CHANGED', 'AUDIT_REQUIRED', 'SOURCE_UNAVAILABLE', 'ARCHIVED', 'ERROR')),
    checked_at      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS releases (
    id                     INTEGER PRIMARY KEY,
    version                TEXT NOT NULL UNIQUE,
    source_commit          TEXT NOT NULL,
    release_date           TEXT NOT NULL,
    artifact_hash          TEXT NOT NULL,
    signing_key_fingerprint TEXT,
    audit_reference        TEXT,
    static_gate_passed     INTEGER NOT NULL DEFAULT 0 CHECK (static_gate_passed = 1),
    runtime_tested         INTEGER NOT NULL DEFAULT 0 CHECK (runtime_tested = 0),
    release_status         TEXT NOT NULL
                           CHECK (release_status IN ('PRE_RELEASE', 'STABLE', 'WITHDRAWN')),
    notes                  TEXT
);

CREATE TABLE IF NOT EXISTS decisions (
    id                       INTEGER PRIMARY KEY,
    decision_id              TEXT NOT NULL UNIQUE,
    patch_id                 INTEGER NOT NULL REFERENCES patches(id) ON DELETE RESTRICT,
    previous_status          TEXT NOT NULL,
    new_status               TEXT NOT NULL,
    decision_reason          TEXT NOT NULL,
    evidence                 TEXT NOT NULL DEFAULT '[]',
    decision_date            TEXT NOT NULL,
    approved_by              TEXT NOT NULL,
    requires_manual_approval INTEGER NOT NULL DEFAULT 1 CHECK (requires_manual_approval = 1),
    scope                    TEXT
                             CHECK (scope IN ('DISTRIBUTION', 'CATALOG_VISIBILITY', 'POLICY_EXCEPTION'))
);

-- Append-only history. No UPDATE or DELETE for audits, findings and decisions.
CREATE TRIGGER IF NOT EXISTS audits_no_update
BEFORE UPDATE ON audits
BEGIN
    SELECT RAISE(ABORT, 'audits are append-only');
END;

CREATE TRIGGER IF NOT EXISTS audits_no_delete
BEFORE DELETE ON audits
BEGIN
    SELECT RAISE(ABORT, 'audits are append-only');
END;

CREATE TRIGGER IF NOT EXISTS findings_no_update
BEFORE UPDATE ON findings
BEGIN
    SELECT RAISE(ABORT, 'findings are append-only');
END;

CREATE TRIGGER IF NOT EXISTS findings_no_delete
BEFORE DELETE ON findings
BEGIN
    SELECT RAISE(ABORT, 'findings are append-only');
END;

CREATE TRIGGER IF NOT EXISTS decisions_no_update
BEFORE UPDATE ON decisions
BEGIN
    SELECT RAISE(ABORT, 'decisions are append-only');
END;

CREATE TRIGGER IF NOT EXISTS decisions_no_delete
BEFORE DELETE ON decisions
BEGIN
    SELECT RAISE(ABORT, 'decisions are append-only');
END;

CREATE TRIGGER IF NOT EXISTS source_revisions_no_update
BEFORE UPDATE ON source_revisions
BEGIN
    SELECT RAISE(ABORT, 'source_revisions are append-only');
END;

CREATE TRIGGER IF NOT EXISTS source_revisions_no_delete
BEFORE DELETE ON source_revisions
BEGIN
    SELECT RAISE(ABORT, 'source_revisions are append-only');
END;

-- Indexes.
CREATE INDEX IF NOT EXISTS idx_patches_application ON patches(application_id);
CREATE INDEX IF NOT EXISTS idx_patches_source ON patches(source_id);
CREATE INDEX IF NOT EXISTS idx_patches_audit_status ON patches(audit_status);
CREATE INDEX IF NOT EXISTS idx_patches_distribution_status ON patches(distribution_status);
CREATE INDEX IF NOT EXISTS idx_audits_patch ON audits(patch_id);
CREATE INDEX IF NOT EXISTS idx_findings_audit ON findings(audit_id);
CREATE INDEX IF NOT EXISTS idx_dependencies_patch ON dependencies(patch_id);
CREATE INDEX IF NOT EXISTS idx_compatibility_patch ON compatibility_assessments(patch_id);
CREATE INDEX IF NOT EXISTS idx_update_checks_source ON update_checks(source_id);
CREATE INDEX IF NOT EXISTS idx_decisions_patch ON decisions(patch_id);
