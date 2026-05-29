import pandas as pd
from scheduler import Scheduler

def main():
    print("Initializing Scheduler...")
    try:
        scheduler = Scheduler("faculty.xlsx", "classroom.xlsx")
    except FileNotFoundError:
        print("Error: Could not find data files. Did you run generate_data.py first?")
        return

    print("Generating Timetable...")
    timetable_df = scheduler.generate_timetable()

    output_file = "timetable_output.xlsx"
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Save complete flat view
        timetable_df['Day_Categorical'] = pd.Categorical(timetable_df['Day'], categories=days_order, ordered=True)
        timetable_df_sorted = timetable_df.sort_values(['Classroom', 'Day_Categorical', 'Slot']).drop('Day_Categorical', axis=1)
        
        timetable_df_sorted.to_excel(writer, sheet_name='Flat View All', index=False)
        
        # Iterate and print per classroom
        classrooms = sorted(list(timetable_df["Classroom"].unique()))
        
        for c in classrooms:
            df_c = timetable_df[timetable_df["Classroom"] == c].copy()
            df_c["Cell"] = df_c["Subject"] + "\n(" + df_c["Faculty"] + ")"
            weekly_view = df_c.pivot(index="Slot", columns="Day", values="Cell")
            weekly_view = weekly_view[days_order]
            
            print("\n" + "="*80)
            print(f"GENERATED TIMETABLE ({c})")
            print("="*80)
            print(weekly_view.to_markdown())
            
            # Save to Excel
            sheet_name = f"Grid-{c}"
            weekly_view.to_excel(writer, sheet_name=sheet_name[:31])
            
    print("\n" + "="*80)
    print(f"Timetables successfully exported to {output_file}")
    print("="*80)

if __name__ == "__main__":
    main()
