import os
import pathlib

structure = {
    ".": [
        "README.md",
        ".gitignore",
        ".env.example",
        "docker-compose.yml",
        "docker-compose.prod.yml",
    ],
    "frontend": [
        "package.json",
        "next.config.js",
        "tailwind.config.js",
        "tsconfig.json",
        ".env.local.example",
    ],
    "frontend/public/assets/icons": [],
    "frontend/public/assets/images": [],
    "frontend/src/app": [
        "layout.tsx",
        "page.tsx",
    ],
    "frontend/src/app/(citizen)/login": ["page.tsx"],
    "frontend/src/app/(citizen)/report": ["page.tsx"],
    "frontend/src/app/(citizen)/report/confirm": ["page.tsx"],
    "frontend/src/app/(citizen)/complaints": ["page.tsx"],
    "frontend/src/app/(citizen)/complaints/[id]": ["page.tsx"],
    "frontend/src/app/(citizen)/feedback/[id]": ["page.tsx"],
    "frontend/src/app/(officer)/login": ["page.tsx"],
    "frontend/src/app/(officer)/dashboard": ["page.tsx"],
    "frontend/src/app/(officer)/incidents/[id]": ["page.tsx"],
    "frontend/src/app/(officer)/incidents/[id]/resolve": ["page.tsx"],
    "frontend/src/app/(admin)/login": ["page.tsx"],
    "frontend/src/app/(admin)/command-center": ["page.tsx"],
    "frontend/src/app/(admin)/live-map": ["page.tsx"],
    "frontend/src/app/(admin)/complaints": ["page.tsx"],
    "frontend/src/app/(admin)/departments": ["page.tsx"],
    "frontend/src/app/(admin)/officers": ["page.tsx"],
    "frontend/src/app/(admin)/sla-monitoring": ["page.tsx"],
    "frontend/src/app/(admin)/analytics": ["page.tsx"],
    "frontend/src/app/(admin)/ai-monitoring": ["page.tsx"],
    "frontend/src/app/(admin)/configuration": ["page.tsx"],
    "frontend/src/components/shared": [
        "Button.tsx",
        "StatusBadge.tsx",
        "PriorityBadge.tsx",
        "MapView.tsx",
        "HeatmapLayer.tsx",
        "EvidenceUploader.tsx",
    ],
    "frontend/src/components/citizen": [
        "ReportForm.tsx",
        "ClassificationPreview.tsx",
        "StatusTimeline.tsx",
    ],
    "frontend/src/components/officer": [
        "IncidentQueue.tsx",
        "SLATimer.tsx",
        "BeforeAfterUpload.tsx",
    ],
    "frontend/src/components/admin": [
        "KPICard.tsx",
        "DepartmentPerformanceChart.tsx",
        "AIConfidenceChart.tsx",
    ],
    "frontend/src/lib": [
        "api-client.ts",
        "auth.ts",
        "constants.ts",
    ],
    "frontend/src/hooks": [
        "useComplaints.ts",
        "useIncidents.ts",
        "useSLATimer.ts",
    ],
    "frontend/src/types": [
        "index.ts",
    ],
    "backend": [
        "requirements.txt",
        "pyproject.toml",
        ".env.example",
        "alembic.ini",
        "main.py",
    ],
    "backend/app/core": [
        "config.py",
        "security.py",
        "database.py",
        "logging.py",
        "exceptions.py",
    ],
    "backend/app/middleware": [
        "auth_middleware.py",
        "rbac_middleware.py",
        "rate_limit_middleware.py",
        "audit_middleware.py",
    ],
    "backend/app/modules/users": [
        "models.py",
        "schemas.py",
        "routes.py",
        "service.py",
    ],
    "backend/app/modules/complaints": [
        "models.py",
        "schemas.py",
        "routes.py",
        "service.py",
    ],
    "backend/app/modules/incidents": [
        "models.py",
        "schemas.py",
        "routes.py",
        "service.py",
    ],
    "backend/app/modules/routing": [
        "models.py",
        "schemas.py",
        "routes.py",
        "service.py",
    ],
    "backend/app/modules/assignments": [
        "models.py",
        "schemas.py",
        "routes.py",
        "service.py",
    ],
    "backend/app/modules/sla": [
        "models.py",
        "schemas.py",
        "routes.py",
        "service.py",
    ],
    "backend/app/modules/field_actions": [
        "models.py",
        "schemas.py",
        "routes.py",
        "service.py",
    ],
    "backend/app/modules/feedback": [
        "models.py",
        "schemas.py",
        "routes.py",
        "service.py",
    ],
    "backend/app/modules/notifications": [
        "models.py",
        "schemas.py",
        "routes.py",
        "service.py",
    ],
    "backend/app/modules/analytics": [
        "schemas.py",
        "routes.py",
        "service.py",
    ],
    "backend/app/services": [
        "storage_service.py",
        "geo_service.py",
        "ai_client.py",
    ],
    "backend/app/utils": [
        "validators.py",
        "pagination.py",
        "id_generator.py",
    ],
    "backend/app/tests": [
        "conftest.py",
        "test_complaints.py",
        "test_routing.py",
        "test_sla.py",
        "test_incidents.py",
    ],
    "ai": [
        "requirements.txt",
        "__init__.py",
        "config.py",
        "gateway.py",
    ],
    "ai/classification": [
        "text_classifier.py",
        "image_classifier.py",
        "speech_to_text.py",
    ],
    "ai/classification/prompts": [
        "classification_prompt.md",
        "severity_prompt.md",
    ],
    "ai/duplicate_detection": [
        "embeddings.py",
        "similarity.py",
        "clustering.py",
    ],
    "ai/severity_scoring": [
        "scorer.py",
        "explainability.py",
    ],
    "ai/resolution_verification": [
        "verifier.py",
    ],
    "ai/evaluation": [
        "classification_metrics.py",
        "duplicate_metrics.py",
        "sample_review.py",
    ],
    "ai/tests": [
        "test_text_classifier.py",
        "test_duplicate_detection.py",
        "test_severity_scoring.py",
    ],
    "database/migrations/versions": [],
    "database/seeds": [
        "seed_departments.py",
        "seed_zones_wards.py",
        "seed_demo_complaints.py",
    ],
    "database": [
        "schema.sql",
    ],
    "scripts": [
        "setup_dev.sh",
        "run_migrations.sh",
        "seed_demo_data.sh",
        "generate_ticket_ids.py",
    ],
    "docs": [
        "architecture.md",
        "api-reference.md",
        "database-schema.md",
        "deployment-guide.md",
        "demo-script.md",
    ],
    "deployment/docker": [
        "frontend.Dockerfile",
        "backend.Dockerfile",
        "ai.Dockerfile",
    ],
    "deployment/nginx": [
        "nginx.conf",
    ],
    "deployment/ci": [
        "github-actions.yml",
    ],
}

base_dir = r"c:\Users\Lenovo\Downloads\risklens"

for folder, files in structure.items():
    folder_path = os.path.join(base_dir, folder)
    os.makedirs(folder_path, exist_ok=True)
    for file in files:
        file_path = os.path.join(folder_path, file)
        # Create empty file
        pathlib.Path(file_path).touch()

print("Scaffolding completed successfully.")
