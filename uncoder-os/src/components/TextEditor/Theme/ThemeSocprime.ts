/* eslint-disable */
import ace from 'ace-builds/src-noconflict/ace';
import './ThemeSocprime.sass';


ace.define('ace/theme/socprime', ['require', 'exports', 'module', 'ace/lib/dom'], (require: any, exports: any, module: any) => {
  exports.isDark = true;
  exports.cssClass = 'ace-socprime';
  exports.cssText = '';
  exports.$selectionColorConflict = true;

  const dom = require('ace/lib/dom');
  dom.importCssString(exports.cssText, exports.cssClass, false);
}); (function () {
  ace.require(['ace/theme/socprime'], (m: any) => {
    if (typeof module === 'object' && typeof exports === 'object' && module) {
      module.exports = m;
    }
  });
}());
