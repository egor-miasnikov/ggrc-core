/*!
 Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 Created By: Aliaksandr_Novik3@epam.com
 Maintained By: Aliaksandr_Novik3@epam.com
 */

describe('can.mustache.helper.page_info', function () {
  'use strict';

  var helper;

  beforeAll(function () {
    helper = can.Mustache._helpers.page_info.fn;
  });

  it('return info about visible items on page', function () {
    var result;
    result = helper(15, 10, 3000);
    expect(result).toEqual("141-150 items of 3000 total");
  });
});
