import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown2
import streamlit as st

def generate_summarised_video_section(video, summary):
  section_html = f"""
      <td style="width: 50%; padding: 10px; box-sizing: border-box; vertical-align: top;">
          <img src="{video['thumbnail']}" alt="thumbnail" style="width: 100%;">
          <h3>👉 <a href="#" target="_blank">{video['title']}</a></h3>
          <p>🤖 AI-Generated actionables from video:</p>
          <div style="font-size: 10px;">
            {markdown2.markdown(summary)}
          </div>
          <a href="https://www.youtube.com/watch?v={video['video_id']}" target="_blank">👀 Watch original Video</a>
      </td>
  """
  return section_html

def generate_email_template(sender_email, subject, summarised_sections):
    # Image URL saved on Imgur
    banner_url = "https://i.imgur.com/wUoeb87.gif"

    rows = []

    for i in range(0, len(summarised_sections), 2):
        row_sections = summarised_sections[i:i+2]
        row_html = '<tr>' + ''.join(row_sections) + '</tr>'
        rows.append(row_html)

    all_rows = ''.join(rows)

    html_body = f"""
    <html>
        <body style="font-family: 'Roboto', sans-serif; font-size: 16px;">
            <img src="{banner_url}" alt="Banner Image" style="width: 100%;"><br>
            <p>These are the summaries of videos published by your fave channels this month!</p>
            <table width="100%" cellspacing="0" cellpadding="0" style="border-collapse: collapse;">
                {all_rows}
            </table>
            <footer>
                <p>Sign up to <a href="fairylightsai.substack.com" target="_blank">100GenAI project newsletter</a> to learn how to build AI projects like this! ✨🤖🧪</p>
            </footer>
        </body>
    </html>
    """

    # Create the MIMEMultipart message
    message = MIMEMultipart('related')
    message['From'] = sender_email
    message['Subject'] = subject
    message.attach(MIMEText(html_body, 'html'))

    return message


def send_email(sender_email, subscribers, content):
    password = st.secrets["smtp"]["app_password"]
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # For TLS

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Start TLS encryption

    try:
        server.login(sender_email, password)
        subscriber_list = subscribers.split(",")

        for receiver_email in subscriber_list:
            receiver_email = receiver_email.strip()
            content['To'] = receiver_email
            server.sendmail(sender_email, receiver_email, content.as_string())
            print(f"Email sent successfully to {receiver_email}")

    except smtplib.SMTPServerDisconnected:
        print("SMTP server disconnected. Reconnecting...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        server.quit()