## Pramas: env, short_env, notify_type, fragment_type, ack_link
## TODO: use include mako page

%if fragment_type == 'title':
    ${title(env, notify_type)}
%elif fragment_type == 'content':
    %if notify_type in ('email', 'pushover', 'sms', 'pushbullet'):
        ${plain_content(env, notify_type)}
    %elif notify_type in ('telegram', 'wework'):
        ${title(env, notify_type)}
        |
        ${markdown_content(env, notify_type)}
    %else:
        ${title(env, notify_type)}
        |
        ${plain_content(env, notify_type)}
    %endif
%endif


<%def name="title(env, notify_type)" >
<%
    archive_hint = '[ICINGA ARCHIVE] ' if env.NOTIFICATION_IS_ARCHIVE else ''
%>
%if env.TARGET_TYPE == 'host':
## ${env.NOTIFICATIONTYPE - $HOSTDISPLAYNAME is $HOSTSTATE
    %if notify_type == 'wework':
        %if env.NAGIOS_NOTIFICATIONTYPE == 'RECOVERY':
<font color="info">Host ${env.NAGIOS_HOSTSTATE} alert for ${env.NAGIOS_HOSTNAME}(${env.NAGIOS__HOSTLOC}: ${env.NAGIOS__HOSTWANIP})!</font>
        %elif env.NAGIOS_NOTIFICATIONTYPE == 'PROBLEM':
<font color="warning">Host ${env.NAGIOS_HOSTSTATE} alert for ${env.NAGIOS_HOSTNAME}(${env.NAGIOS__HOSTLOC}: ${env.NAGIOS__HOSTWANIP})!</font>
        %else:
<font color="comment">Host ${env.NAGIOS_HOSTSTATE} alert for ${env.NAGIOS_HOSTNAME}(${env.NAGIOS__HOSTLOC}: ${env.NAGIOS__HOSTWANIP})!/font>
        %endif
    %elif notify_type == 'telegram':
Host `${env.NAGIOS_HOSTSTATE}` alert for ${env.NAGIOS_HOSTNAME}(${env.NAGIOS__HOSTLOC}: ${env.NAGIOS__HOSTWANIP})!
    %else:
${archive_hint}Host ${env.NAGIOS_HOSTSTATE} alert for ${env.NAGIOS_HOSTNAME}(${env.NAGIOS__HOSTLOC}: ${env.NAGIOS__HOSTWANIP})!
    %endif

%elif env.TARGET_TYPE == 'service':

## $NOTIFICATIONTYPE - $HOSTDISPLAYNAME - $SERVICEDISPLAYNAME is $SERVICESTATE
    %if notify_type == 'wework':
        %if env.NAGIOS_NOTIFICATIONTYPE == 'RECOVERY':
<font color="info">${env.NAGIOS_NOTIFICATIONTYPE} - ${env.NAGIOS_HOSTALIAS}/${env.NAGIOS_SERVICEDESC} is ${env.NAGIOS_SERVICESTATE}</font>
        %elif env.NAGIOS_NOTIFICATIONTYPE == 'PROBLEM':
<font color="warning">${env.NAGIOS_NOTIFICATIONTYPE} - ${env.NAGIOS_HOSTALIAS}/${env.NAGIOS_SERVICEDESC} is ${env.NAGIOS_SERVICESTATE}</font>
        %else:
<font color="comment">${env.NAGIOS_NOTIFICATIONTYPE} - ${env.NAGIOS_HOSTALIAS}/${env.NAGIOS_SERVICEDESC} is ${env.NAGIOS_SERVICESTATE}</font>
        %endif
    %elif notify_type == 'telegram':
`${env.NAGIOS_NOTIFICATIONTYPE}` - ${env.NAGIOS_HOSTALIAS}/${env.NAGIOS_SERVICEDESC} is `${env.NAGIOS_SERVICESTATE}`
    %else:
${archive_hint}${env.NAGIOS_NOTIFICATIONTYPE} - ${env.NAGIOS_HOSTALIAS}/${env.NAGIOS_SERVICEDESC} is ${env.NAGIOS_SERVICESTATE}
    %endif

%endif
</%def>



<%def name="plain_content(env, notify_type)" >
%if env.TARGET_TYPE == 'host':
    %if notify_type == 'sms':

## "$NOTIFICATIONTYPE$: Host $HOSTSTATE$ alert for $HOSTNAME$($_HOSTLOC$: $_HOSTWANIP$)!"
${short_env.type}: ${short_env.host} ${short_env.hoststate}, ${short_env.time}, ${short_env.extra}, ${short_env.link}

    %elif notify_type == 'email':

***** Icinga  *****
|
Notification Type: ${env.NOTIFICATIONTYPE}
|
Host: ${env.HOSTALIAS}
Address: ${env.HOSTADDRESS}
State: ${env.HOSTSTATE}
|
Date/Time: ${env.LONGDATETIME}
|
Additional Info: ${env.HOSTOUTPUT}
|
Comment: [${env.NOTIFICATIONAUTHORNAME}] ${env.NOTIFICATIONCOMMENT}

    %else:

Notification Type: ${env.NAGIOS_NOTIFICATIONTYPE}
Host: ${env.NAGIOS_HOSTALIAS}
Duration: ${env.NAGIOS_HOSTDURATION}
Date/Time: ${env.NAGIOS_LONGDATETIME}
Additional Info:
${env.NAGIOS_HOSTOUTPUT}
${env.NAGIOS_LONGHOSTOUTPUT}
        %if env.NOTIFICATIONAUTHORNAME:
Comment: [${env.NOTIFICATIONAUTHORNAME}] ${env.NOTIFICATIONCOMMENT}
        %endif

    %endif
%elif env.TARGET_TYPE == 'service':
    %if notify_type == 'sms':

## "$NOTIFICATIONTYPE$: $HOSTALIAS$/$SERVICEDESC$ is $SERVICESTATE$: $SERVICEOUTPUT$ $LONGSERVICEOUTPUT$"
${short_env.type}: ${short_env.host}/${short_env.service}, ${short_env.time}, ${short_env.extra}, ${short_env.link}

    %elif notify_type == 'email':

***** Icinga  *****
|
Notification Type: ${env.NOTIFICATIONTYPE}
|
Service: ${env.SERVICEDESC}
Host: ${env.HOSTALIAS}
Address: ${env.HOSTADDRESS}
State: ${env.SERVICESTATE}
|
Date/Time: ${env.LONGDATETIME}
|
Additional Info: ${env.SERVICEOUTPUT}
|
Comment: [${env.NOTIFICATIONAUTHORNAME}] ${env.NOTIFICATIONCOMMENT}
|
Link: ${icinga_link}

    %else:

${short_env.time}
${'Duration: %s' % env.NAGIOS_SERVICEDURATION if env.SERVICE_DURATION_SEC and float(env.SERVICE_DURATION_SEC) > 1 else ''}
${'Contacts: %s' % env.NAGIOS__SERVICECONTACT if env.NAGIOS__SERVICECONTACT else ''}
Additional Info:
${env.NAGIOS_SERVICEOUTPUT}
${env.NAGIOS_LONGSERVICEOUTPUT}
        %if env.NOTIFICATIONAUTHORNAME:
Comment: [${env.NOTIFICATIONAUTHORNAME}] ${env.NOTIFICATIONCOMMENT}
        %endif

    %endif
%endif

%if short_env.custom_wiki_url:
Wiki: ${short_env.custom_wiki_url}
%elif short_env.wiki_base_url and short_env.service:
Wiki: ${short_env.wiki_base_url}/${short_env.service}
%endif

%if ack_link:
Acknowledge: ${ack_link}
%endif
%if reboot_host_link:
QuickReboot: ${reboot_host_link}
%endif
</%def>


<%def name="markdown_content(env, notify_type)" >
%if env.TARGET_TYPE == 'host':

**${env.NAGIOS_NOTIFICATIONTYPE}**
Host: ${env.NAGIOS_HOSTALIAS}
Duration: ${env.NAGIOS_HOSTDURATION}
Date/Time: ${env.NAGIOS_LONGDATETIME}
Additional Info:
    %if notify_type == 'wework':
        %if env.NAGIOS_HOSTOUTPUT:
> ${env.NAGIOS_HOSTOUTPUT}
        %endif
        %if env.NAGIOS_LONGHOSTOUTPUT:
> ${env.NAGIOS_LONGHOSTOUTPUT}
        %endif
|
    %elif notify_type == 'telegram':
```
${env.NAGIOS_HOSTOUTPUT}
${env.NAGIOS_LONGHOSTOUTPUT}
```
    %else:
${env.NAGIOS_HOSTOUTPUT}
${env.NAGIOS_LONGHOSTOUTPUT}
    %endif

    %if env.NOTIFICATIONAUTHORNAME:
Comment: [${env.NOTIFICATIONAUTHORNAME}] ${env.NOTIFICATIONCOMMENT}
    %endif

%elif env.TARGET_TYPE == 'service':

${short_env.time}
${'Duration: %s' % env.NAGIOS_SERVICEDURATION if env.SERVICE_DURATION_SEC and float(env.SERVICE_DURATION_SEC) > 1 else ''}
${'Contacts: %s' % env.NAGIOS__SERVICECONTACT if env.NAGIOS__SERVICECONTACT else ''}
Additional Info:
    %if notify_type == 'wework':
        %if env.NAGIOS_SERVICEOUTPUT:
> ${env.NAGIOS_SERVICEOUTPUT}
        %endif
        %if env.NAGIOS_LONGSERVICEOUTPUT:
> ${env.NAGIOS_LONGSERVICEOUTPUT}
        %endif
|
    %elif notify_type == 'telegram':
```
${env.NAGIOS_SERVICEOUTPUT}
${env.NAGIOS_LONGSERVICEOUTPUT}
```
    %else:
${env.NAGIOS_SERVICEOUTPUT}
${env.NAGIOS_LONGSERVICEOUTPUT}
    %endif

    %if env.NOTIFICATIONAUTHORNAME:
Comment: [${env.NOTIFICATIONAUTHORNAME}] ${env.NOTIFICATIONCOMMENT}
    %endif

%endif

${wiki_link(short_env)}\
${' | [Acknowledge](%s)' % ack_link if ack_link else ''}\
${' | [QuickReboot](%s)' % reboot_host_link if reboot_host_link else ''}
</%def>

<%def name="wiki_link(short_env)" >
%if short_env.custom_wiki_url:
[Wiki](${short_env.custom_wiki_url})\
%elif short_env.wiki_base_url and short_env.service:
[Wiki](${short_env.wiki_base_url}/${short_env.service})\
%endif
</%def>
