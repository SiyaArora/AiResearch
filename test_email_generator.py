#!/usr/bin/env python3
"""
Test script for Tuition Remission Email Generator
Uses CSV data instead of Oracle database for testing

This script demonstrates the email generation functionality
without requiring an Oracle database connection.
"""

import csv
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_csv_data(csv_file: str) -> list:
    """Load data from CSV file"""
    records = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert column names to match database format
                record = {
                    'employee_name': row.get('Employee_Name', ''),
                    'employee_id': row.get('Employee_ID', ''),
                    'employee_email': row.get('Employee_Email', ''),
                    'letter_date': row.get('Letter_Date', ''),
                    'student_name': row.get('Student_Name', ''),
                    'student_id': row.get('Student_ID', ''),
                    'relation_to_employee': row.get('Relation_To_Employee', ''),
                    'level': row.get('Level', ''),
                    'major': row.get('Major', ''),
                    'college': row.get('College', ''),
                    'degree': row.get('Degree', ''),
                    'intersession': row.get('Intersession', '0'),
                    'spring': row.get('Spring', '0'),
                    'summer': row.get('Summer', '0'),
                    'fall': row.get('Fall', '0'),
                    'total_benefit': row.get('Total_Benefit', '0'),
                    'less_qualified_exemption': row.get('Less_Qualified_Exemption', '0'),
                    'ytd_taxed_amount': row.get('YTD_Taxed_Amount', '0'),
                    'taxable_benefit_balance': row.get('Taxable_Benefit_Balance', '0'),
                    'taxable_benefit_per_pay_period': row.get('Taxable_Benefit_Per_Pay_Period', '0'),
                    'estimated_net_reduction_per_pay': row.get('Estimated_Net_Reduction_Per_Pay', '0'),
                    'pay_period_start_date': row.get('Pay_Period_Start_Date', ''),
                }
                records.append(record)

        logger.info(f"Loaded {len(records)} records from CSV")
        return records

    except Exception as e:
        logger.error(f"Error loading CSV: {e}")
        return []


def format_currency(amount: float) -> str:
    """Format number as currency string"""
    try:
        if amount is None or amount == '':
            return "$0.00"
        # Remove commas and convert to float
        amount_str = str(amount).replace(',', '')
        amount_float = float(amount_str)
        return f"${amount_float:,.2f}"
    except:
        return "$0.00"


def format_date(date_value) -> str:
    """Format date as string"""
    if isinstance(date_value, datetime):
        return date_value.strftime("%B %d, %Y")
    return str(date_value)


def generate_html_email(data: dict, usf_green: str = "#00543C", usf_gold: str = "#FDBB30") -> str:
    """Generate HTML email from tuition data"""

    # Extract and format data
    employee_name = data.get('employee_name', 'Employee')
    student_name = data.get('student_name', '')
    relation = data.get('relation_to_employee', '')
    major = data.get('major', '')
    degree = data.get('degree', '')
    college = data.get('college', '')

    # Financial data - handle various formats
    try:
        intersession = float(str(data.get('intersession', 0) or 0).replace(',', ''))
        spring = float(str(data.get('spring', 0) or 0).replace(',', ''))
        summer = float(str(data.get('summer', 0) or 0).replace(',', ''))
        fall = float(str(data.get('fall', 0) or 0).replace(',', ''))
        total_benefit = float(str(data.get('total_benefit', 0) or 0).replace(',', ''))
        exemption = float(str(data.get('less_qualified_exemption', 0) or 0).replace(',', ''))
        ytd_taxed = float(str(data.get('ytd_taxed_amount', 0) or 0).replace(',', ''))
        taxable_balance = float(str(data.get('taxable_benefit_balance', 0) or 0).replace(',', ''))
        per_pay_period = float(str(data.get('taxable_benefit_per_pay_period', 0) or 0).replace(',', ''))
        net_reduction = float(str(data.get('estimated_net_reduction_per_pay', 0) or 0).replace(',', ''))
    except:
        intersession = spring = summer = fall = 0
        total_benefit = exemption = ytd_taxed = taxable_balance = 0
        per_pay_period = net_reduction = 0

    # Dates
    letter_date = format_date(data.get('letter_date', datetime.now()))
    pay_start_date = format_date(data.get('pay_period_start_date', ''))

    # Generate HTML (same as original)
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tuition Remission Notification</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, Helvetica, sans-serif; background-color: #f4f4f4;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f4f4f4;">
        <tr>
            <td align="center" style="padding: 40px 20px;">
                <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">

                    <!-- Header with USF Branding -->
                    <tr>
                        <td style="background-color: {usf_green}; padding: 30px 40px; border-radius: 8px 8px 0 0;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: normal;">
                                University of San Francisco
                            </h1>
                            <p style="margin: 5px 0 0 0; color: {usf_gold}; font-size: 14px; font-weight: 500;">
                                Office of Human Resources
                            </p>
                        </td>
                    </tr>

                    <!-- Main Content -->
                    <tr>
                        <td style="padding: 40px;">
                            <h2 style="margin: 0 0 20px 0; color: #333333; font-size: 20px;">
                                Tuition Remission - Intersession/Spring 2026
                            </h2>

                            <p style="margin: 0 0 20px 0; color: #555555; font-size: 16px; line-height: 1.6;">
                                Dear {employee_name},
                            </p>

                            <p style="margin: 0 0 20px 0; color: #555555; font-size: 14px; line-height: 1.6;">
                                As an employee who is using the USF Tuition Remission Benefits program this semester for yourself and/or dependents, this is a reminder that the tuition remission benefit is subject to the applicable state, federal, and local taxes under provisions of the Internal Revenue Code and the California Revenue and Taxation Code. In accordance with these requirements, taxes for this semester are being processed in the February through April pay periods.
                            </p>

                            <p style="margin: 0 0 20px 0; color: #555555; font-size: 14px; line-height: 1.6;">
                                According to Strategic Enrollment Management, you have received tuition for the student and program listed below. If this tuition remission is for you (and not your dependent) the otherwise taxable amount of your tuition has been reduced by $5,250.00 (which is permitted by Section 127 of the Internal Revenue Code).
                            </p>

                            <!-- Student Information Box -->
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f8f9fa; border-radius: 6px; margin: 25px 0; border-left: 4px solid {usf_green};">
                                <tr>
                                    <td style="padding: 25px;">
                                        <h3 style="margin: 0 0 15px 0; color: {usf_green}; font-size: 16px; font-weight: bold;">
                                            Student/Program Information
                                        </h3>
                                        <table role="presentation" width="100%" cellspacing="0" cellpadding="6">
                                            <tr>
                                                <td style="color: #666666; font-size: 14px; width: 40%;">Student Name:</td>
                                                <td style="color: #333333; font-size: 14px; font-weight: 600;">{student_name}</td>
                                            </tr>
                                            <tr>
                                                <td style="color: #666666; font-size: 14px;">Relation to Employee:</td>
                                                <td style="color: #333333; font-size: 14px; font-weight: 600;">{relation}</td>
                                            </tr>
                                            <tr>
                                                <td style="color: #666666; font-size: 14px;">Major:</td>
                                                <td style="color: #333333; font-size: 14px;">{major}</td>
                                            </tr>
                                            <tr>
                                                <td style="color: #666666; font-size: 14px;">College:</td>
                                                <td style="color: #333333; font-size: 14px;">{college}</td>
                                            </tr>
                                            <tr>
                                                <td style="color: #666666; font-size: 14px;">Degree:</td>
                                                <td style="color: #333333; font-size: 14px;">{degree}</td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>

                            <p style="margin: 20px 0 10px 0; color: #555555; font-size: 14px; line-height: 1.6;">
                                After deducting taxable benefits already processed, this leaves a taxable benefit balance per student/program as outlined below:
                            </p>

                            <!-- Financial Summary Box -->
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f8f9fa; border-radius: 6px; margin: 25px 0;">
                                <tr>
                                    <td style="padding: 25px;">
                                        <h3 style="margin: 0 0 15px 0; color: {usf_green}; font-size: 16px; border-bottom: 2px solid {usf_green}; padding-bottom: 10px; font-weight: bold;">
                                            Tuition Benefit Summary
                                        </h3>
                                        <table role="presentation" width="100%" cellspacing="0" cellpadding="8">
                                            <tr>
                                                <td style="color: #555555; font-size: 14px;">Intersession:</td>
                                                <td align="right" style="color: #333333; font-size: 14px; font-weight: 600;">{format_currency(intersession)}</td>
                                            </tr>
                                            <tr>
                                                <td style="color: #555555; font-size: 14px;">Spring:</td>
                                                <td align="right" style="color: #333333; font-size: 14px; font-weight: 600;">{format_currency(spring)}</td>
                                            </tr>
                                            <tr>
                                                <td style="color: #555555; font-size: 14px;">Summer:</td>
                                                <td align="right" style="color: #333333; font-size: 14px; font-weight: 600;">{format_currency(summer)}</td>
                                            </tr>
                                            <tr>
                                                <td style="color: #555555; font-size: 14px;">Fall:</td>
                                                <td align="right" style="color: #333333; font-size: 14px; font-weight: 600;">{format_currency(fall)}</td>
                                            </tr>
                                            <tr style="border-top: 1px solid #dee2e6;">
                                                <td style="color: #333333; font-size: 14px; font-weight: bold; padding-top: 12px;">Total Benefit:</td>
                                                <td align="right" style="color: #333333; font-size: 14px; font-weight: bold; padding-top: 12px;">{format_currency(total_benefit)}</td>
                                            </tr>
                                            <tr>
                                                <td style="color: #555555; font-size: 14px;">Less Qualified Exemption:</td>
                                                <td align="right" style="color: #333333; font-size: 14px; font-weight: 600;">{format_currency(exemption)}</td>
                                            </tr>
                                            <tr>
                                                <td style="color: #555555; font-size: 14px;">YTD Taxed Amount:</td>
                                                <td align="right" style="color: #333333; font-size: 14px; font-weight: 600;">{format_currency(ytd_taxed)}</td>
                                            </tr>
                                            <tr style="background-color: rgba(0, 84, 60, 0.1);">
                                                <td style="color: {usf_green}; font-size: 16px; font-weight: bold; padding-top: 12px;">Taxable Benefit Balance:</td>
                                                <td align="right" style="color: {usf_green}; font-size: 18px; font-weight: bold; padding-top: 12px;">{format_currency(taxable_balance)}</td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>

                            <!-- Pay Period Information -->
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #fff8e1; border-left: 4px solid {usf_gold}; margin: 25px 0;">
                                <tr>
                                    <td style="padding: 20px;">
                                        <p style="margin: 0 0 10px 0; color: #333333; font-size: 14px; line-height: 1.6;">
                                            This total taxable benefit amount will be added to your gross wages at the rate of <strong>{format_currency(per_pay_period)}</strong> per pay period. This may result in a net pay reduction as estimated below. The estimate is based on a 37.25% tax rate, which includes state, federal, and local income and employment tax rates.
                                        </p>
                                        <table role="presentation" width="100%" cellspacing="0" cellpadding="6" style="margin-top: 15px;">
                                            <tr>
                                                <td style="color: #666666; font-size: 13px;">Total Taxable Benefit Balance:</td>
                                                <td align="right" style="color: #333333; font-size: 13px; font-weight: bold;">{format_currency(taxable_balance)}</td>
                                            </tr>
                                            <tr>
                                                <td style="color: #666666; font-size: 13px;">Pay Period Start Date:</td>
                                                <td align="right" style="color: #333333; font-size: 13px; font-weight: bold;">{pay_start_date}</td>
                                            </tr>
                                            <tr>
                                                <td style="color: #666666; font-size: 13px;">Taxable Benefit Per Pay Period:</td>
                                                <td align="right" style="color: #333333; font-size: 13px; font-weight: bold;">{format_currency(per_pay_period)}</td>
                                            </tr>
                                            <tr style="background-color: rgba(253, 187, 48, 0.2);">
                                                <td style="color: #d97706; font-size: 14px; font-weight: bold; padding-top: 8px;">Estimated Net Reduction Per Pay:</td>
                                                <td align="right" style="color: #d97706; font-size: 14px; font-weight: bold; padding-top: 8px;">{format_currency(net_reduction)}</td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>

                            <p style="margin: 20px 0; color: #555555; font-size: 14px; line-height: 1.6;">
                                This total taxable benefit amount will be added to your calendar year gross wages which will be reported on Form W-2 to the IRS and the California Franchise Tax Board.
                            </p>

                            <p style="margin: 20px 0; color: #555555; font-size: 14px; line-height: 1.6;">
                                Please feel free to contact me with any questions at <a href="mailto:tuitionremission@usfca.edu" style="color: {usf_green}; text-decoration: none; font-weight: 600;">tuitionremission@usfca.edu</a>.
                            </p>

                            <!-- Action Button -->
                            <table role="presentation" cellspacing="0" cellpadding="0" style="margin: 30px 0;">
                                <tr>
                                    <td style="background-color: {usf_green}; border-radius: 6px;">
                                        <a href="https://myusf.usfca.edu/hr/benefits/tuition-remission" target="_blank" style="display: inline-block; padding: 14px 30px; color: #ffffff; text-decoration: none; font-size: 16px; font-weight: bold;">
                                            View Tuition Remission Information
                                        </a>
                                    </td>
                                </tr>
                            </table>

                            <p style="margin: 20px 0 0 0; color: #555555; font-size: 14px; line-height: 1.6;">
                                Thank you,<br>
                                <strong>Diane Sweeney</strong><br>
                                Human Resources
                            </p>
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 25px 40px; border-radius: 0 0 8px 8px; border-top: 1px solid #eeeeee;">
                            <p style="margin: 0 0 10px 0; color: #888888; font-size: 12px; line-height: 1.5;">
                                University of San Francisco<br>
                                Human Resources - Benefits Office<br>
                                2130 Fulton Street, San Francisco, CA 94117
                            </p>
                            <p style="margin: 0; color: #888888; font-size: 11px;">
                                This is an automated notification regarding your tuition remission benefits.<br>
                                For questions, contact HR Benefits at (415) 422-6457 or tuitionremission@usfca.edu
                            </p>
                        </td>
                    </tr>

                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""

    return html


def generate_test_emails(csv_file: str, output_dir: str = "test_emails", limit: int = None):
    """
    Generate test emails from CSV data

    Args:
        csv_file: Path to CSV file
        output_dir: Directory to save generated emails
        limit: Number of emails to generate (None = all)
    """
    # Load CSV data
    records = load_csv_data(csv_file)

    if not records:
        logger.error("No records found in CSV")
        return

    # Limit records if specified
    if limit:
        records = records[:limit]
        logger.info(f"Limiting to first {limit} records")

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Generate emails
    count = 0
    for record in records:
        try:
            # Generate HTML
            html_content = generate_html_email(record)

            # Create filename
            employee_id = record.get('employee_id', 'unknown')
            employee_name = record.get('employee_name', 'employee')
            safe_name = "".join(c for c in employee_name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_name = safe_name.replace(' ', '_')

            filename = f"{employee_id}_{safe_name}_tuition_remission.html"
            filepath = output_path / filename

            # Save email
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)

            logger.info(f"Generated email for {employee_name} ({employee_id})")
            count += 1

        except Exception as e:
            logger.error(f"Error generating email for record: {e}")
            continue

    print(f"\n{'='*60}")
    print(f"Test email generation complete!")
    print(f"Generated {count} HTML emails")
    print(f"Output directory: {output_dir}/")
    print(f"{'='*60}\n")
    print(f"To view emails, open the HTML files in a web browser:")
    print(f"  Example: open {output_dir}/{list(output_path.glob('*.html'))[0].name if list(output_path.glob('*.html')) else 'first_email.html'}")
    print()


def main():
    """Main test function"""

    # CSV file from previous step
    csv_file = "tuition_remission_data.csv"

    # Check if CSV exists
    if not Path(csv_file).exists():
        print(f"Error: CSV file '{csv_file}' not found.")
        print("Please run the CSV generation script first.")
        return

    print("="*60)
    print("Tuition Remission Email Generator - TEST MODE")
    print("="*60)
    print()
    print("This test will generate HTML emails from your CSV data.")
    print()

    # Ask user how many to generate
    try:
        user_input = input("How many test emails to generate? (press Enter for all): ").strip()
        limit = int(user_input) if user_input else None
    except ValueError:
        limit = None

    print()

    # Generate test emails
    generate_test_emails(
        csv_file=csv_file,
        output_dir="test_emails",
        limit=limit
    )


if __name__ == "__main__":
    main()
