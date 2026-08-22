from services.learning_plan_service import create_learning_plan


plan = create_learning_plan(
    source="sample_cv.txt",
    target_role="Junior Backend Developer",
    current_level="Başlangıç",
    weekly_hours=7,
    duration_weeks=4,
)

print("\nÖĞRENME PLANI")
print("-" * 70)
print(plan)
print("-" * 70)