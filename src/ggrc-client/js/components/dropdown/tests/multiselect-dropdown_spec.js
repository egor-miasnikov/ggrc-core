/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import {getComponentVM} from '../../../../js_specs/spec_helpers';
import Component from '../multiselect-dropdown';

describe('multiselect-dropdown component', function () {
  'use strict';

  let events;
  let viewModel;

  beforeAll(function () {
    events = Component.prototype.events;
  });

  beforeEach(function () {
    viewModel = getComponentVM(Component);
  });

  describe('openDropdown() method', function () {
    it('sets "canBeOpen" to true if component is not disabled', function () {
      viewModel.attr('canBeOpen', false);
      viewModel.attr('disabled', false);

      viewModel.openDropdown();

      expect(viewModel.attr('canBeOpen')).toBe(true);
    });

    it('does not set "canBeOpen" if component is disabled', function () {
      viewModel.attr('canBeOpen', false);
      viewModel.attr('disabled', true);

      viewModel.openDropdown();

      expect(viewModel.attr('canBeOpen')).toBe(false);
    });
  });

  describe('events', function () {
    describe('"{window} click" handler', function () {
      let method;
      let that;

      beforeEach(function () {
        that = {
          viewModel: viewModel,
        };
        method = events['{window} click'].bind(that);
      });

      it('calls changeOpenCloseState if component is not disabled',
        function () {
          viewModel.changeOpenCloseState =
          jasmine.createSpy('changeOpenCloseState');
          viewModel.attr('disabled', false);

          method();

          expect(viewModel.changeOpenCloseState).toHaveBeenCalled();
        });

      it('does not call changeOpenCloseState if component is disabled',
        function () {
          viewModel.changeOpenCloseState =
          jasmine.createSpy('changeOpenCloseState');
          viewModel.attr('disabled', true);

          method();

          expect(viewModel.changeOpenCloseState).not.toHaveBeenCalled();
        });
    });
  });
});
