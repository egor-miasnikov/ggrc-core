/*!
  Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: Egor_Miasnikov@epam.com
  Maintained By: Egor_Miasnikov@epam.com
*/

describe('can.Model.Assessment', function () {
  'use strict';

  var Assessment;
  
  beforeAll(function () {
    Assessment = CMS.Models.Assessment;
  });

  describe('_generate_pagination_request_params() method', function () {

    var defaultRequestObject;
    beforeEach(function () {
      defaultRequestObject = {
        __page: 1,
        __page_size: 5,
        __search: '',
        __sort: 'title|description_inline|name|email',
        __sort_desc: false
      };
    });

    it('returns the object with params for request', function () {
      var result;
      var originObject = {
        page: 2,
        page_size: 10
      };

      var expectedRequestObject = {
        __page: 2,
        __page_size: 10,
        __search: '',
        __sort: 'title|description_inline|name|email',
        __sort_desc: false
      };

      result = Assessment._generate_pagination_request_params(originObject);
      expect(result).toEqual(expectedRequestObject);
    });

    it('returns default params if it gets empty object', function () {
      var result;
      var originObject = {};

      var expectedRequestObject = {
        __page: 1,
        __page_size: 5,
        __search: '',
        __sort: 'title|description_inline|name|email',
        __sort_desc: false
      };

      result = Assessment._generate_pagination_request_params(originObject);
      expect(result).toEqual(expectedRequestObject);
    });
  });

  describe('findAll() method', function () {

    it("makes a call on backend with specific url", function() {
      spyOn($, 'ajax').and.callFake(function (req) {
        var deffered = $.Deferred();
        expect(req.url).toEqual('/api/assessments');
        deffered.resolve({});
        return deffered.promise();
      });

      Assessment.findAll({});
    });
  });
});
