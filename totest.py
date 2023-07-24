import streamlit as st
import pandas as pd

# Step 1: Read Rules from Excel
def read_rules_from_excel(file_path):
    rules_df = pd.read_excel(file_path)  # Assuming the Excel file contains the rules
    return rules_df

# Step 2: Evaluate Rules and Determine Colors
def evaluate_rules_and_determine_colors(input_data_df, rules_df):
    colors = []
    for _, row in input_data_df.iterrows():
        for _, rule_row in rules_df.iterrows():
            condition = rule_row['Condition']
            try:
                if eval(condition, {}, row.to_dict()):
                    colors.append(rule_row['Color'])
                    break
            except Exception as e:
                print(f"Error evaluating condition: {condition}")
                print(f"Error message: {str(e)}")
        else:
            colors.append('Grey')
    return colors

# Step 3: Display Customer Data with Colors
def display_customer_data_with_colors(input_data_df, colors):
    input_data_df['Color'] = colors

    # Function to set font color based on the 'Color' column
    def set_font_color(val):
        return f"color: {val};"

    st.write("Result:")
    st.dataframe(input_data_df.style.applymap(set_font_color, subset=['Color']))

if __name__ == '__main__':
    st.title("Credit Rules Evaluation")

    # Step 1: Read Rules from Excel
    rules_df = read_rules_from_excel(r"C:\Users\ROSHAN DAVID\OneDrive\Desktop\New\credit_rules.xlsx")

    # Step 2: Get Input Data from User using a Form
    st.header("Enter Customer Details:")
    customer_name = st.text_input("Name:")
    age = st.number_input("Age:", min_value=0, max_value=120, step=1)
    credit_score = st.number_input("Credit Score:", min_value=0, max_value=1000, step=1)
    income = st.number_input("Income:", min_value=0, step=1)
    employment_status = st.selectbox("Employment Status:", ["Employed", "Unemployed", "Self-Employed"])
    debt_amount = st.number_input("Debt Amount:", min_value=0, step=1)
    # Add other input fields as needed

    # When the user clicks the "Submit" button, the following code will run
    if st.button("Submit"):
        # Step 3: Evaluate Rules and Determine Colors
        input_data_dict = [
            {
                'Name': customer_name,
                'Age': age,
                'credit_score': credit_score,
                'Income': income,
                'Employment Status': employment_status,
                'Debt Amount': debt_amount
            }
            # Add other rows to the input_data_dict for additional data
        ]

        input_data_df = pd.DataFrame(input_data_dict)

        colors = evaluate_rules_and_determine_colors(input_data_df, rules_df)

        # Step 4: Display Customer Data with Colors
        display_customer_data_with_colors(input_data_df, colors)
