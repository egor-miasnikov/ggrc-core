/*!
  Copyright (C) 2016 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.treePagination', function () {
  'use strict';
  var helpers;
  var scope;

  beforeAll(function () {
    var Component = GGRC.Components.get('treePagination');
    helpers = Component.prototype.helpers;
    scope = Component.prototype.scope;
  });

  beforeEach(function () {
    scope.paging = {
      attr: function (key, value) {
        if (key && !value) {
          return this[key];
        } else if (key && value) {
          this[key] = value;
        } else {
          return;
        }
      },
      current: 1,
      pageSize: 10,
      count: 3
    };
  });

  describe('paginationInfo() method in helpers', function () {
    it('returns info about visible items on page', function () {
      var result;
      result = helpers.paginationInfo(15, 10, 3000);
      expect(result).toEqual('141-150 of 3000 items');
    });

    it('returns "No records" if we don\'t have elements', function () {
      var result;
      result = helpers.paginationInfo(1, 0, 0);
      expect(result).toEqual('No records');
    });
  });
  describe('paginationPlaceholder() method in helpers', function () {
    it('returns placeholder into page input', function () {
      var result;
      result = helpers.paginationPlaceholder(2, 10);
      expect(result).toEqual('Page 2 of 10');
    });
    it('returns empty string if we don\'t have amount of pages', function () {
      var result;
      result = helpers.paginationPlaceholder(2, 0);
      expect(result).toEqual('');
    });
    it('returns "Wrong value" if current page bigger than amount of pages',
      function () {
        var result;
        result = helpers.paginationPlaceholder(10, 2);
        expect(result).toEqual('Wrong value');
      });
  });
  describe('nextPage() method ', function () {
    it('changes current and increase it by 1', function () {
      scope.nextPage();
      expect(scope.paging.current).toEqual(2);
    });
    it('doesn\'t change current value if current equal amount of pages',
      function () {
        scope.paging.current = 3;
        scope.nextPage();
        expect(scope.paging.current).toEqual(3);
      });
  });
  describe('prevPage() method ', function () {
    it('changes current and decrease it by 1', function () {
      scope.paging.current = 2;
      scope.prevPage();
      expect(scope.paging.current).toEqual(1);
    });
    it('doesn\'t change current value if current equal 1',
      function () {
        scope.paging.current = 1;
        scope.prevPage();
        expect(scope.paging.current).toEqual(1);
      });
  });
  describe('firstPage() method ', function () {
    it('changes current if current more than 1', function () {
      scope.paging.current = 3;
      scope.firstPage();
      expect(scope.paging.current).toEqual(1);
    });
  });
  describe('lastPage() method ', function () {
    it('changes current if current less than amount of pages', function () {
      scope.paging.current = 2;
      scope.lastPage();
      expect(scope.paging.current).toEqual(3);
    });
  });
  describe('changePageSize() method ', function () {
    it('changes current to first page and page size', function () {
      scope.paging.current = 2;
      expect(scope.paging.pageSize).toEqual(10);
      scope.changePageSize(25);
      expect(scope.paging.pageSize).toEqual(25);
      expect(scope.paging.current).toEqual(1);
    });
  });
  describe('setCurrentPage() method ', function () {
    var input;
    beforeEach(function () {
      input = {
        value: null,
        val: function () {
          return this.value;
        },
        blur: jasmine.createSpy()
      };
    });
    it('changes current if value more than 1 and less than amount of pages',
      function () {
        input.value = 2;
        scope.setCurrentPage({}, input);
        expect(scope.paging.current).toEqual(2);
      });
    it('changes current to 1 if value less than 1', function () {
      input.value = -1;
      scope.setCurrentPage({}, input);
      expect(scope.paging.current).toEqual(1);
    });
    it('changes current to last if value more than amount of pages',
      function () {
        input.value = 5;
        scope.setCurrentPage({}, input);
        expect(scope.paging.current).toEqual(3);
      });
    it('changes current to 1 if value is NaN',
      function () {
        input.value = 'test word';
        scope.setCurrentPage({}, input);
        expect(scope.paging.current).toEqual(1);
      });
  });
});
