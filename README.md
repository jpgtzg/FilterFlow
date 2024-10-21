# FilterFlow

FilterFlow is a powerful, fast, and fully customizable solution for automating file filtering in emails based on subject lines and attached files. It's designed as an efficient alternative to PowerAutomate, offering greater control and flexibility for users who need streamlined automation for managing their inboxes.

## Features

- **Automated File Filtering**: Automatically process emails, categorize attachments, and sort based on custom rules tied to subject lines and file types.
- **Fast and Efficient**: Optimized for speed, handling high volumes of emails with minimal processing time.
- **Customizable Rules**: Easily create, modify, and extend your filtering rules to suit your unique email management needs.
- **Attachment Management**: Identify and extract specific types of attachments based on file extensions or names.
- **Lightweight and Scalable**: Built to handle everything from personal inboxes to large-scale enterprise email environments.
- **Privacy Focused**: Keep your data secure by running the solution on your own infrastructure without relying on third-party services.

## Why FilterFlow?

Unlike traditional automation platforms like PowerAutomate, FilterFlow puts the user in full control. Whether you need a simple filter for managing your personal inbox or advanced sorting mechanisms for professional use, FilterFlow's flexibility and efficiency make it the perfect solution.

## Getting Started

### Prerequisites

Before using FilterFlow, ensure you have the following installed:

- Python 3.7 or higher
- Required Python libraries:
  - `imaplib2`
  - `email`

You can install the required libraries using the following command:

```bash
pip install imaplib2 email
```

### Installation

Clone the repository:

```bash
git clone https://github.com/jpgtzg/FilterFlow.git
cd FilterFlow
```

### Configuration

1. **Email Configuration**: Update the `config.py` file with your email credentials and server details (e.g., Gmail, Outlook). You can also configure custom rules for filtering emails based on subject or attachment types.
   
   ```python
   EMAIL_ADDRESS = "your-email@example.com"
   EMAIL_PASSWORD = "your-password"
   IMAP_SERVER = "imap.example.com"
   ```

2. **Filter Rules**: Customize the filtering logic in `filter_rules.py`. You can define what subjects to look for and how to handle files:

   ```python
   SUBJECT_RULES = ["Invoice", "Report", "Order"]
   FILE_EXTENSIONS = [".pdf", ".csv", ".xlsx"]
   ```

### Usage

To run FilterFlow, execute the following command:

```bash
python main.py
```

FilterFlow will connect to your email server, process incoming emails, and apply the filtering rules you've defined.

### Example

You can define rules to:
- Filter emails with the subject "Invoice" and save all `.pdf` attachments to a designated folder.
- Ignore emails with specific keywords in the subject line.
- Automatically flag emails with certain types of attachments.

```python
# Example in filter_rules.py

SUBJECT_RULES = ["Invoice", "Report"]
IGNORE_RULES = ["Advertisement", "Newsletter"]
FILE_EXTENSIONS = [".pdf", ".docx"]

def custom_filter(subject, attachments):
    if "Urgent" in subject:
        print("High priority email detected!")
    return True
```

## Customization

FilterFlow is highly customizable:
- **Custom Actions**: Define specific actions for filtered emails, such as forwarding, saving to a folder, or sending an alert.
- **Complex Filters**: Write advanced logic to handle more complex scenarios, such as multi-step processing for attachments or keywords in the body of the email.

## Contributions

Contributions are welcome! If you'd like to add features or fix bugs, feel free to submit a pull request or open an issue.

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-new-filter`).
3. Commit your changes (`git commit -m 'Add a new filter'`).
4. Push to the branch (`git push origin feature-new-filter`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
