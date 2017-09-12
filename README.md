# Simple Mail server

Attempt to implement personal mail server using `python + aiosmtpd`

## Preparation

Clone the project:
```bash
git clone git@github.com:denself/simple_mail_server.git
cd simple_mail_server
```

Before running server, create virtual environment:
```bash
python3.6 -m venv venv
source venv/bin/activate
```

You might need to install `venv` before running this commands:
```bash
apt install python3.6-venv
```

And install all requirements:
```bash
pip install -r requirements.txt
```

## Running server

Server support two optional settings, that cen be changed using environment 
variables:

`SMTP_HOST` defines host, on which server accepts connections. `*` for all.

Keep in mind, that if you setting `SMTP_HOST=::1`, that you should setup DNS 
record that supports IPv6.


`SMTP_PORT` defines servers port. Default ports for SMTP are 25, 2525, 587 and 
465, 25, 587, 2526 for Secure SMTP
 
To start server just run:
```bash
./main.py
```


## DNS settings

To properly handle incoming mail, two DNS record necessary:

- One `A` Record, that points to your mail server
```
mx.example.com   A   1.2.3.4
```
    
- Another on `MX` record, that points to previous `A` record.
```
example.com      MX   mx.example.com
``` 

TODO: SPF/DKIM/DMARC records
https://www.namecheap.com/support/knowledgebase/article.aspx/317/2237/how-do-i-add-txtspfdkimdmarc-records-for-my-domain


## Supervisor

Install supervisor: 
```bash
apt install supervisor
```

Copy file `supervisor.ini` to you supervisor's `conf.d` directory:

```bash
cp supervisor.conf /etc/supervisor/conf.d/smtp_server.conf
```

Edit all variables to match your environment.

Start server:

```bash
supervisorctl reread
supervisorctl update
supervisorctl start smtp-server
```
    
    