# Endpoint mapping

| cdmon endpoint | Method |
|---|---|
| `status` | `status(action)` |
| `check` | `check(domain)` |
| `info` | `info(domain, authcode=None)` |
| `authcode` | `authcode(domain)` |
| `domains/list` | `list_domains(extended_info=True)` |
| `register` | `register(domain, period, intended_use, contact)` |
| `renew` | `renew(domain, period)` |
| `transfer` | `transfer(domain, authcode)` |
| `restore` | `restore(domain)` |
| `block` | `set_block(domain, enabled)` |
| `whoisprivate` | `set_whois_private(domain, enabled)` |
| `dnssec` | `set_dnssec(domain, enabled)` |
| `dns` | `set_nameservers(domain, nameservers)` |
| `getDnsRecords` | `get_dns_records(domain)` |
| `dnsrecords/create` | `create_dns_record(domain, record)` |
| `dnsrecords/edit` | `edit_dns_record(domain, current, new)` |
| `dnsrecords/delete` | `delete_dns_record(domain, host, type_)` |
| `sendDnsKey` | `send_dns_key(...)` |
| `getPrice` | `get_price(tld, action)` |
| `getPeriods` | `get_periods(tld, action)` |
| `autorenewal` | `get_autorenewal(domain)` |
| `autorenewal/manage` | `manage_autorenewal(...)` |
| `balance` | `balance()` |
| `contacts/modify` | `modify_contact(payload)` |
