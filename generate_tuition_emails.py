#!/usr/bin/env python3
"""
Tuition Remission Email Generator
Extracts data from Oracle database and generates branded HTML emails
"""

import cx_Oracle
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TuitionEmailGenerator:
    """Generates tuition remission emails from Oracle database data"""

    # Brand colors
    USF_GREEN = "#00543C"
    USF_GOLD = "#FDBB30"

    def __init__(self, db_config: Dict[str, str]):
        """
        Initialize the email generator

        Args:
            db_config: Dictionary with database connection parameters
                      Keys: username, password, host, port, service_name
        """
        self.db_config = db_config
        self.connection = None

    def connect_to_database(self) -> bool:
        """
        Establish connection to Oracle database

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            dsn = cx_Oracle.makedsn(
                self.db_config['host'],
                self.db_config['port'],
                service_name=self.db_config['service_name']
            )

            self.connection = cx_Oracle.connect(
                user=self.db_config['username'],
                password=self.db_config['password'],
                dsn=dsn,
                encoding="UTF-8"
            )

            logger.info("Successfully connected to Oracle database")
            return True

        except cx_Oracle.Error as error:
            logger.error(f"Error connecting to Oracle database: {error}")
            return False

    def fetch_tuition_data(self, table_name: str = "contact_tuition") -> List[Dict]:
        """
        Fetch tuition remission data from Oracle database

        Args:
            table_name: Name of the table to query (default: contact_tuition)

        Returns:
            List of dictionaries containing employee tuition data
        """
        if not self.connection:
            logger.error("No database connection established")
            return []

        try:
            cursor = self.connection.cursor()

            # Query to fetch tuition data
            # Adjust column names based on your actual table structure
            query = f"""
                SELECT
                    employee_name,
                    employee_id,
                    employee_email,
                    letter_date,
                    student_name,
                    student_id,
                    relation_to_employee,
                    level,
                    major,
                    college,
                    degree,
                    intersession,
                    spring,
                    summer,
                    fall,
                    total_benefit,
                    less_qualified_exemption,
                    ytd_taxed_amount,
                    taxable_benefit_balance,
                    taxable_benefit_per_pay_period,
                    estimated_net_reduction_per_pay,
                    pay_period_start_date
                FROM {table_name}
                ORDER BY employee_name
            """

            cursor.execute(query)
            columns = [col[0].lower() for col in cursor.description]

            results = []
            for row in cursor:
                results.append(dict(zip(columns, row)))

            logger.info(f"Fetched {len(results)} records from {table_name}")
            cursor.close()

            return results

        except cx_Oracle.Error as error:
            logger.error(f"Error fetching data: {error}")
            return []

    def format_currency(self, amount: float) -> str:
        """Format number as currency string"""
        if amount is None:
            return "$0.00"
        return f"${amount:,.2f}"

    def format_date(self, date_value) -> str:
        """Format date as string"""
        if isinstance(date_value, datetime):
            return date_value.strftime("%B %d, %Y")
        return str(date_value)

    def generate_html_email(self, data: Dict) -> str:
        """
        Generate HTML email from tuition data

        Args:
            data: Dictionary containing employee and tuition information

        Returns:
            HTML string for the email
        """
        # Extract and format data
        employee_name = data.get('employee_name', 'Employee')
        student_name = data.get('student_name', '')
        relation = data.get('relation_to_employee', '')
        major = data.get('major', '')
        degree = data.get('degree', '')
        college = data.get('college', '')

        # Financial data
        intersession = float(data.get('intersession', 0) or 0)
        spring = float(data.get('spring', 0) or 0)
        summer = float(data.get('summer', 0) or 0)
        fall = float(data.get('fall', 0) or 0)
        total_benefit = float(data.get('total_benefit', 0) or 0)
        exemption = float(data.get('less_qualified_exemption', 0) or 0)
        ytd_taxed = float(data.get('ytd_taxed_amount', 0) or 0)
        taxable_balance = float(data.get('taxable_benefit_balance', 0) or 0)
        per_pay_period = float(data.get('taxable_benefit_per_pay_period', 0) or 0)
        net_reduction = float(data.get('estimated_net_reduction_per_pay', 0) or 0)

        # Dates
        letter_date = self.format_date(data.get('letter_date', datetime.now()))
        pay_start_date = self.format_date(data.get('pay_period_start_date', ''))

        # Generate HTML
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
                        <td style="background-color: {self.USF_GREEN}; padding: 30px 40px; border-radius: 8px 8px 0 0;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: normal;">
                                University of San Francisco
                            </h1>
                            <p style="margin: 5px 0 0 0; color: {self.USF_GOLD}; font-size: 14px; font-weight: 500;">
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
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f8f9fa; border-radius: 6px; margin: 25px 0; border-left: 4px solid {self.USF_GREEN};">
                                <tr>
                                    <td style="padding: 25px;">
                                        <h3 style="margin: 0 0 15px 0; color: {self.USF_GREEN}; font-size: 16px; font-weight: bold;">
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
                                        <h3 style="margin: 0 0 15px 0; color: {self.USF_GREEN}; font-size: 16px; border-bottom: 2px solid {self.USF_GREEN}; padding-bottom: 10px; font-weight: bold;">
                                            Tuition Benefit Summary
                                        </h3>
                                        <table role="presentation" width="100%" cellspacing="0" cellpadding="8">
                                            <tr>
                                                <td style="color: #555555; font-size: 14px;">Intersession:</td>
                                                <td align="right" style="color: #333333; font-size: 14px; font-weight: 600;">{self.format_currency(intersession)}</td>
                                            </tr>
                                            <tr>
                                                <td style="color: #555555; font-size: 14px;">Spring:</td>
                                                <td align="right" style="color: #333333; font-size: 14px; font-weight: 600;">{self.format_currency(spring)}</td>
                                            </tr>
                                            <tr>
                                                <td style="color: #555555; font-size: 14px;">Summer:</td>
                                                <td align="right" style="color: #333333; font-size: 14px; font-weight: 600;">{self.format_currency(summer)}</td>
                                            </tr>
                                            <tr>
                                                <td style="color: #555555; font-size: 14px;">Fall:</td>
                                                <td align="right" style="color: #333333; font-size: 14px; font-weight: 600;">{self.format_currency(fall)}</td>
                                            </tr>
                                            <tr style="border-top: 1px solid #dee2e6;">
                                                <td style="color: #333333; font-size: 14px; font-weight: bold; padding-top: 12px;">Total Benefit:</td>
                                                <td align="right" style="color: #333333; font-size: 14px; font-weight: bold; padding-top: 12px;">{self.format_currency(total_benefit)}</td>
                                            </tr>
                                            <tr>
                                                <td style="color: #555555; font-size: 14px;">Less Qualified Exemption:</td>
                                                <td align="right" style="color: #333333; font-size: 14px; font-weight: 600;">{self.format_currency(exemption)}</td>
                                            </tr>
                                            <tr>
                                                <td style="color: #555555; font-size: 14px;">YTD Taxed Amount:</td>
                                                <td align="right" style="color: #333333; font-size: 14px; font-weight: 600;">{self.format_currency(ytd_taxed)}</td>
                                            </tr>
                                            <tr style="background-color: rgba(0, 84, 60, 0.1);">
                                                <td style="color: {self.USF_GREEN}; font-size: 16px; font-weight: bold; padding-top: 12px;">Taxable Benefit Balance:</td>
                                                <td align="right" style="color: {self.USF_GREEN}; font-size: 18px; font-weight: bold; padding-top: 12px;">{self.format_currency(taxable_balance)}</td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>

                            <!-- Pay Period Information -->
                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #fff8e1; border-left: 4px solid {self.USF_GOLD}; margin: 25px 0;">
                                <tr>
                                    <td style="padding: 20px;">
                                        <p style="margin: 0 0 10px 0; color: #333333; font-size: 14px; line-height: 1.6;">
                                            This total taxable benefit amount will be added to your gross wages at the rate of <strong>{self.format_currency(per_pay_period)}</strong> per pay period. This may result in a net pay reduction as estimated below. The estimate is based on a 37.25% tax rate, which includes state, federal, and local income and employment tax rates.
                                        </p>
                                        <table role="presentation" width="100%" cellspacing="0" cellpadding="6" style="margin-top: 15px;">
                                            <tr>
                                                <td style="color: #666666; font-size: 13px;">Total Taxable Benefit Balance:</td>
                                                <td align="right" style="color: #333333; font-size: 13px; font-weight: bold;">{self.format_currency(taxable_balance)}</td>
                                            </tr>
                                            <tr>
                                                <td style="color: #666666; font-size: 13px;">Pay Period Start Date:</td>
                                                <td align="right" style="color: #333333; font-size: 13px; font-weight: bold;">{pay_start_date}</td>
                                            </tr>
                                            <tr>
                                                <td style="color: #666666; font-size: 13px;">Taxable Benefit Per Pay Period:</td>
                                                <td align="right" style="color: #333333; font-size: 13px; font-weight: bold;">{self.format_currency(per_pay_period)}</td>
                                            </tr>
                                            <tr style="background-color: rgba(253, 187, 48, 0.2);">
                                                <td style="color: #d97706; font-size: 14px; font-weight: bold; padding-top: 8px;">Estimated Net Reduction Per Pay:</td>
                                                <td align="right" style="color: #d97706; font-size: 14px; font-weight: bold; padding-top: 8px;">{self.format_currency(net_reduction)}</td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>

                            <p style="margin: 20px 0; color: #555555; font-size: 14px; line-height: 1.6;">
                                This total taxable benefit amount will be added to your calendar year gross wages which will be reported on Form W-2 to the IRS and the California Franchise Tax Board.
                            </p>

                            <p style="margin: 20px 0; color: #555555; font-size: 14px; line-height: 1.6;">
                                Please feel free to contact me with any questions at <a href="mailto:tuitionremission@usfca.edu" style="color: {self.USF_GREEN}; text-decoration: none; font-weight: 600;">tuitionremission@usfca.edu</a>.
                            </p>

                            <!-- Action Button -->
                            <table role="presentation" cellspacing="0" cellpadding="0" style="margin: 30px 0;">
                                <tr>
                                    <td style="background-color: {self.USF_GREEN}; border-radius: 6px;">
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

    def generate_all_emails(self, output_dir: str = "emails", table_name: str = "contact_tuition") -> int:
        """
        Generate HTML emails for all records in the database

        Args:
            output_dir: Directory to save generated emails
            table_name: Name of the database table

        Returns:
            Number of emails generated
        """
        # Fetch data
        records = self.fetch_tuition_data(table_name)

        if not records:
            logger.warning("No records found to process")
            return 0

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Generate emails
        count = 0
        for record in records:
            try:
                # Generate HTML
                html_content = self.generate_html_email(record)

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

        logger.info(f"Successfully generated {count} emails in {output_dir}/")
        return count

    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")


def main():
    """Main execution function"""

    # Database configuration
    # IMPORTANT: Update these values with your actual database credentials
    db_config = {
        'username': 'your_username',
        'password': 'your_password',
        'host': 'your_host',
        'port': '1521',  # Default Oracle port
        'service_name': 'your_service_name'
    }

    # Alternative: Read from environment variables for security
    # db_config = {
    #     'username': os.getenv('ORACLE_USER'),
    #     'password': os.getenv('ORACLE_PASSWORD'),
    #     'host': os.getenv('ORACLE_HOST'),
    #     'port': os.getenv('ORACLE_PORT', '1521'),
    #     'service_name': os.getenv('ORACLE_SERVICE')
    # }

    # Initialize generator
    generator = TuitionEmailGenerator(db_config)

    try:
        # Connect to database
        if generator.connect_to_database():
            # Generate emails
            # Update table_name if different from default
            count = generator.generate_all_emails(
                output_dir="tuition_emails_output",
                table_name="contact_tuition"
            )

            print(f"\n{'='*60}")
            print(f"Email generation complete!")
            print(f"Generated {count} HTML emails")
            print(f"Output directory: tuition_emails_output/")
            print(f"{'='*60}\n")
        else:
            print("Failed to connect to database. Please check your credentials.")

    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise

    finally:
        # Always close the connection
        generator.close_connection()


if __name__ == "__main__":
    main()
