-- CreateEnum
CREATE TYPE "life_phase" AS ENUM ('dreamer', 'explorer', 'builder', 'driver', 'sage', 'philosopher');

-- CreateEnum
CREATE TYPE "permission" AS ENUM ('view_profiles', 'edit_profiles', 'manage_assessments', 'send_invites', 'assign_programs', 'admin_access');

-- CreateEnum
CREATE TYPE "user_permission_type" AS ENUM ('admin', 'editor', 'viewer');

-- CreateEnum
CREATE TYPE "user_role" AS ENUM ('nextie', 'agency', 'program', 'military', 'admin', 'partner', 'guardian', 'alumni');

-- CreateEnum
CREATE TYPE "user_segment" AS ENUM ('high_school', 'out_of_school_youth', 'college_enrolled', 'military_service', 'reentry', 'adult_learner', 'refugee_or_migrant', 'underemployed', 'alumni_returning', 'international');

-- CreateTable
CREATE TABLE "achievements" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "user_id" UUID,
    "code" TEXT,
    "description" TEXT,
    "date_earned" TIMESTAMPTZ(6),
    "bonus_credits" INTEGER DEFAULT 0,

    CONSTRAINT "achievements_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "assessment_framework" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "user_id" UUID,
    "date" TIMESTAMPTZ(6) NOT NULL,
    "version" TEXT,
    "completion_rate" INTEGER,
    "reliability" TEXT,
    "question_count" INTEGER,
    "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
    "primary_assessment_tier_id" UUID,

    CONSTRAINT "assessment_framework_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "assessment_questions" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "prompt" TEXT NOT NULL,
    "category" TEXT,
    "tier" TEXT,
    "type" TEXT,
    "tags" TEXT[],
    "weight" DOUBLE PRECISION DEFAULT 1.0,
    "is_active" BOOLEAN DEFAULT true,
    "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "assessment_questions_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "audit_log" (
    "id" UUID NOT NULL,
    "user_id" UUID,
    "action" TEXT,
    "table_affected" TEXT,
    "record_id" UUID,
    "changed_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
    "change_details" JSONB,

    CONSTRAINT "audit_log_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "gamification_state" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "user_id" UUID,
    "cosmic_credits" INTEGER DEFAULT 0,
    "level" INTEGER DEFAULT 1,
    "streak_days" INTEGER DEFAULT 0,
    "last_activity" TIMESTAMPTZ(6),

    CONSTRAINT "gamification_state_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "micro_assessments" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "user_id" UUID,
    "type" TEXT,
    "questions_count" INTEGER,
    "completed_at" TIMESTAMPTZ(6),
    "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "micro_assessments_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "micro_responses" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "micro_assessment_id" UUID,
    "question_id" UUID,
    "answer" INTEGER,
    "category" TEXT,
    "question_type" TEXT,

    CONSTRAINT "micro_responses_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "organizations" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "name" TEXT NOT NULL,
    "type" TEXT,
    "location" TEXT,

    CONSTRAINT "organizations_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "pathway_tracking" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "user_id" UUID,
    "current_step" TEXT,
    "next_step" TEXT,
    "suggested_by" TEXT,
    "updated_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "pathway_tracking_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "primary_assessment_tier" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "name" TEXT,
    "description" TEXT,
    "color" TEXT,
    "strengths" TEXT,
    "learning_style" TEXT,
    "career_paths" TEXT,

    CONSTRAINT "primary_assessment_tier_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "profile_attributes" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "name" TEXT,
    "score" INTEGER,
    "tier_id" UUID,

    CONSTRAINT "profile_attributes_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "programs" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "name" TEXT NOT NULL,
    "description" TEXT,
    "organization_id" UUID,
    "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "programs_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "rewards" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "name" TEXT,
    "description" TEXT,
    "cost" INTEGER,

    CONSTRAINT "rewards_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "secondary_assessment_tier" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "name" TEXT,
    "description" TEXT,
    "color" TEXT,
    "level" INTEGER,
    "framework_id" UUID,

    CONSTRAINT "secondary_assessment_tier_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "skill_recommendations" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "user_id" UUID,
    "skill_name" TEXT,
    "recommendation_reason" TEXT,
    "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "skill_recommendations_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "star_signature_snapshots" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "user_id" UUID,
    "assessment_framework_id" UUID,
    "snapshot_data" JSONB,
    "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "star_signature_snapshots_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "tertiary_assessment_tier" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "name" TEXT,
    "category" TEXT,
    "color" TEXT,
    "description" TEXT,
    "score" INTEGER,
    "confidence" DOUBLE PRECISION,
    "framework_id" UUID,

    CONSTRAINT "tertiary_assessment_tier_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "user_activity_log" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "user_id" UUID,
    "activity_type" TEXT,
    "details" JSONB,
    "occurred_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "user_activity_log_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "user_org_affiliations" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "user_id" UUID,
    "organization_id" UUID,
    "role" TEXT,
    "status" TEXT,

    CONSTRAINT "user_org_affiliations_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "user_permissions" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "user_id" UUID,
    "permission" "permission" NOT NULL,

    CONSTRAINT "user_permissions_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "user_profile_attributes" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "user_id" UUID,
    "profile_attribute_id" UUID,
    "score" INTEGER,
    "confidence" DOUBLE PRECISION,
    "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "user_profile_attributes_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "user_profiles" (
    "user_id" UUID NOT NULL,
    "birth_year" INTEGER,
    "education_level" TEXT,
    "interests" JSONB,
    "career_goals" JSONB,
    "visibility" TEXT DEFAULT 'private',

    CONSTRAINT "user_profiles_pkey" PRIMARY KEY ("user_id")
);

-- CreateTable
CREATE TABLE "user_role_history" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "user_id" UUID,
    "role" "user_role" NOT NULL,
    "started_at" TIMESTAMP(6) NOT NULL,
    "ended_at" TIMESTAMP(6),

    CONSTRAINT "user_role_history_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "user_secondary_influences" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "user_id" UUID,
    "secondary_tier_id" UUID,
    "level" INTEGER,
    "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "user_secondary_influences_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "user_segments" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "user_id" UUID,
    "segment" "user_segment" NOT NULL,

    CONSTRAINT "user_segments_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "user_tags" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "user_id" UUID,
    "tag" TEXT NOT NULL,

    CONSTRAINT "user_tags_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "user_tags_map" (
    "user_id" UUID NOT NULL,
    "tag" TEXT NOT NULL,

    CONSTRAINT "user_tags_map_pkey" PRIMARY KEY ("user_id","tag")
);

-- CreateTable
CREATE TABLE "users" (
    "id" UUID NOT NULL DEFAULT gen_random_uuid(),
    "name" TEXT NOT NULL,
    "email" TEXT,
    "user_type" TEXT DEFAULT 'STUDENT',
    "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
    "starsyn_image_url" TEXT,

    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "users_email_key" ON "users"("email");

-- AddForeignKey
ALTER TABLE "achievements" ADD CONSTRAINT "achievements_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "assessment_framework" ADD CONSTRAINT "assessment_framework_primary_assessment_tier_id_fkey" FOREIGN KEY ("primary_assessment_tier_id") REFERENCES "primary_assessment_tier"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "assessment_framework" ADD CONSTRAINT "assessment_framework_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "gamification_state" ADD CONSTRAINT "gamification_state_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "micro_assessments" ADD CONSTRAINT "micro_assessments_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "micro_responses" ADD CONSTRAINT "micro_responses_micro_assessment_id_fkey" FOREIGN KEY ("micro_assessment_id") REFERENCES "micro_assessments"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "micro_responses" ADD CONSTRAINT "micro_responses_question_id_fkey" FOREIGN KEY ("question_id") REFERENCES "assessment_questions"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "pathway_tracking" ADD CONSTRAINT "pathway_tracking_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "profile_attributes" ADD CONSTRAINT "profile_attributes_tier_id_fkey" FOREIGN KEY ("tier_id") REFERENCES "tertiary_assessment_tier"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "programs" ADD CONSTRAINT "programs_organization_id_fkey" FOREIGN KEY ("organization_id") REFERENCES "organizations"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "secondary_assessment_tier" ADD CONSTRAINT "secondary_assessment_tier_framework_id_fkey" FOREIGN KEY ("framework_id") REFERENCES "assessment_framework"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "skill_recommendations" ADD CONSTRAINT "skill_recommendations_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "star_signature_snapshots" ADD CONSTRAINT "star_signature_snapshots_assessment_framework_id_fkey" FOREIGN KEY ("assessment_framework_id") REFERENCES "assessment_framework"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "star_signature_snapshots" ADD CONSTRAINT "star_signature_snapshots_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "tertiary_assessment_tier" ADD CONSTRAINT "tertiary_assessment_tier_framework_id_fkey" FOREIGN KEY ("framework_id") REFERENCES "assessment_framework"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "user_activity_log" ADD CONSTRAINT "user_activity_log_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "user_org_affiliations" ADD CONSTRAINT "user_org_affiliations_organization_id_fkey" FOREIGN KEY ("organization_id") REFERENCES "organizations"("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "user_org_affiliations" ADD CONSTRAINT "user_org_affiliations_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "user_permissions" ADD CONSTRAINT "user_permissions_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "user_profile_attributes" ADD CONSTRAINT "user_profile_attributes_profile_attribute_id_fkey" FOREIGN KEY ("profile_attribute_id") REFERENCES "profile_attributes"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "user_profile_attributes" ADD CONSTRAINT "user_profile_attributes_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "user_profiles" ADD CONSTRAINT "user_profiles_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "user_role_history" ADD CONSTRAINT "user_role_history_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "user_secondary_influences" ADD CONSTRAINT "user_secondary_influences_secondary_tier_id_fkey" FOREIGN KEY ("secondary_tier_id") REFERENCES "secondary_assessment_tier"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "user_secondary_influences" ADD CONSTRAINT "user_secondary_influences_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "user_segments" ADD CONSTRAINT "user_segments_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "user_tags" ADD CONSTRAINT "user_tags_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "user_tags_map" ADD CONSTRAINT "user_tags_map_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "users"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
