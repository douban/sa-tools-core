# coding: utf-8

from __future__ import absolute_import

import logging
import smtplib
from email.mime.text import MIMEText

from sa_tools_core.consts import SMTP_SERVER, SYSADMIN_EMAIL

logger = logging.getLogger(__name__)


def send_mail(to_addrs, content, subject='Sent via sa-tools', from_addr=SYSADMIN_EMAIL):
    smtp = smtplib.SMTP(SMTP_SERVER)
    msg = MIMEText(content, 'plain')
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addrs)

    try:
        smtp.sendmail(from_addr, to_addrs, msg.as_string())
        logger.info('sent email to %s, title: %s', to_addrs, subject)
    except Exception:
        raise
    finally:
        smtp.quit()
