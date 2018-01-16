## Copyright (C) 2018 Google Inc.
## Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

.. WARNING! This file is autogenerated and should not be edited manually.

Services
========


% for service in package.services:
${h.title('``%s``' % service.url, '-')}

Methods::

  % if service.readonly:
    GET ${service.url}
    GET ${service.url}/{id}
  % else:
    POST   ${service.url}
    GET    ${service.url}
    GET    ${service.url}/{id}
    PUT    ${service.url}/{id}
    DELETE ${service.url}/{id}
  % endif

Model :class:`${service.model.name}`


POST Example::

    POST ${service.url}/

    Request headers:
      content-type:application/json
      cookie:SACSID=<ID>;
             session=<SessionID>
      x-requested-by:GGRC

    Request body:
    {
      "${service.table_singular}": {
      % for name, res in sorted(service.attributes.items()):
        % if res.create:
        "${name}": ${service.json_value(name)},
        % endif
      % endfor
      }
    }

    Response body:
    {
      "${service.table_singular}": {
      % for name, res in sorted(service.attributes.items()):
        % if res.read:
        "${name}": ${service.json_value(name)},
        % endif
      % endfor
      }
    }

GET Example::


    GET ${service.url}/1

    Request headers:
      content-type:application/json
      cookie:SACSID=<ID>;
             session=<SessionID>
      x-requested-by:GGRC

    Response headers:
      content-type:application/json
      Date:Thu, 30 Mar 2017 10:51:14 GMT
      etag:"d87058b07a1c1efe8bc2949033b5766db239fb9d"

    Response body:
    {
      "${service.table_singular}": {
      % for name, res in sorted(service.attributes.items()):
        % if res.read:
        "${name}": ${service.json_value(name)},
        % endif
      % endfor
      }
    }

PUT Example::

    PUT ${service.url}/1

    Request headers:
      content-type:application/json
      cookie:SACSID=<ID>;
             session=<SessionID>
      if-match:"d87058b07a1c1efe8bc2949033b5766db239fb9d"
      if-unmodified-since:Thu, 30 Mar 2017 10:51:14 GMT
      x-requested-by:GGRC

    Request body:
    {
      "${service.table_singular}": {
      % for name, res in sorted(service.attributes.items()):
        % if res.update:
        "${name}": ${service.json_value(name)},
        % endif
      % endfor
      }
    }

    Response headers:
      content-type:application/json
      date:Mon, 16 Oct 2017 15:10:07 GMT
      etag:"d87058b07a1c1efe8bc2949033b5766db239fb9d"
      last-modified:Thu, 30 Mar 2017 10:51:14 GMT

    Response body:
    {
      "${service.table_singular}": {
      % for name, res in sorted(service.attributes.items()):
        % if res.read:
        "${name}": ${service.json_value(name)},
        % endif
      % endfor
      }
    }

% endfor
