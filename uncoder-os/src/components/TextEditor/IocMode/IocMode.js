/* eslint-disable */
import ace from 'ace-builds/src-noconflict/ace';

import './uncoder-cti-highlighter.sass';
import {
    EMAILS_HIGHLIGHT_PATTERN,
    IP_HIGHLIGHT_PATTERN,
    MD5_HIGHLIGHT_PATTERN,
    SHA1_HIGHLIGHT_PATTERN,
    SHA256_HIGHLIGHT_PATTERN,
    SHA512_HIGHLIGHT_PATTERN,
    URL_DOMAIN_HIGHLIGHT_PATTERN,
} from "../../../constants/IocsInputEditorConstats";

ace.define(
  'ace/mode/uncoder_cti_highlight_rules',
  ['require', 'exports', 'module', 'ace/lib/oop', 'ace/mode/text_highlight_rules'],
  (require, exports) => {
    'use strict';

    let oop = require('../lib/oop');
    let TextHighlightRules = require(
      './text_highlight_rules').TextHighlightRules;

    let UncoderCtiHighlightRules = function () {
      this.$rules = {
        'start': [
          {
            token: ['text', 'ip', 'text'],
            regex: IP_HIGHLIGHT_PATTERN,
          },
          {
            token: ['url', 'domain', 'url'],
            regex: URL_DOMAIN_HIGHLIGHT_PATTERN,
          },
          {
            token: ['emails'],
            regex: EMAILS_HIGHLIGHT_PATTERN,
          },
          {
            token: ['text', 'hash.md5'],
            regex: MD5_HIGHLIGHT_PATTERN,
          },
          {
            token: ['text', 'hash.sha1'],
            regex: SHA1_HIGHLIGHT_PATTERN,
          },
          {
            token: ['text', 'hash.sha256'],
            regex: SHA256_HIGHLIGHT_PATTERN,
          },
          {
            token: ['text', 'hash.sha512'],
            regex: SHA512_HIGHLIGHT_PATTERN,
          },
        ],
      };
      this.normalizeRules();
    };

    oop.inherits(UncoderCtiHighlightRules, TextHighlightRules);

    exports.UncoderCtiHighlightRules = UncoderCtiHighlightRules;
  }
);

ace.define(
  'ace/mode/matching_brace_outdent',
  ['require', 'exports', 'module', 'ace/range'],
  function (require, exports) {
    'use strict';

    let Range = require('../range').Range;

    let MatchingBraceOutdent = function () {
    };

    (function () {

      this.checkOutdent = function (line, input) {
        if (!/^\s+$/.test(line)) {
          return false;
        }

        return /^\s*}/.test(input);
      };

      this.autoOutdent = function (doc, row) {
        let line = doc.getLine(row);
        let match = line.match(/^(\s*})/);

        if (!match) {
          return 0;
        }

        let column = match[1].length;
        let openBracePos = doc.findMatchingBracket({row: row, column: column});

        if (!openBracePos || openBracePos.row === row) {
          return 0;
        }

        let indent = this.$getIndent(doc.getLine(openBracePos.row));
        doc.replace(new Range(row, 0, row, column - 1), indent);
      };

      this.$getIndent = function (line) {
        return line.match(/^\s*/)[0];
      };

    }).call(MatchingBraceOutdent.prototype);

    exports.MatchingBraceOutdent = MatchingBraceOutdent;
  }
);

ace.define(
  'ace/mode/folding/coffee',
  ['require', 'exports', 'module', 'ace/lib/oop', 'ace/mode/folding/fold_mode', 'ace/range'],
  function (require, exports) {
    'use strict';

    let oop = require('../../lib/oop');
    let BaseFoldMode = require('./fold_mode').FoldMode;
    let Range = require('../../range').Range;

    let FoldMode = exports.FoldMode = function () {
    };
    oop.inherits(FoldMode, BaseFoldMode);

    (function () {

      this.getFoldWidgetRange = function (session, foldStyle, row) {
        let range = this.indentationBlock(session, row);
        if (range) {
          return range;
        }

        let re = /\S/;
        let line = session.getLine(row);
        let startLevel = line.search(re);
        if (startLevel === -1 || line[startLevel] !== '#') {
          return;
        }

        let startColumn = line.length;
        let maxRow = session.getLength();
        let startRow = row;
        let endRow = row;

        while (++row < maxRow) {
          line = session.getLine(row);
          let level = line.search(re);

          if (level === -1) {
            continue;
          }

          if (line[level] !== '#') {
            break;
          }

          endRow = row;
        }

        if (endRow > startRow) {
          let endColumn = session.getLine(endRow).length;
          return new Range(startRow, startColumn, endRow, endColumn);
        }
      };
      this.getFoldWidget = function (session, foldStyle, row) {
        let line = session.getLine(row);
        let indent = line.search(/\S/);
        let next = session.getLine(row + 1);
        let prev = session.getLine(row - 1);
        let prevIndent = prev.search(/\S/);
        let nextIndent = next.search(/\S/);

        if (indent === -1) {
          session.foldWidgets[row - 1] =
            prevIndent !== -1 && prevIndent < nextIndent ? 'start' : '';
          return '';
        }
        if (prevIndent === -1) {
          if (indent === nextIndent && line[indent] === '#' && next[indent] ===
            '#') {
            session.foldWidgets[row - 1] = '';
            session.foldWidgets[row + 1] = '';
            return 'start';
          }
        } else if (prevIndent === indent && line[indent] === '#' &&
          prev[indent] === '#') {
          if (session.getLine(row - 2).search(/\S/) === -1) {
            session.foldWidgets[row - 1] = 'start';
            session.foldWidgets[row + 1] = '';
            return '';
          }
        }

        if (prevIndent !== -1 && prevIndent < indent) {
          session.foldWidgets[row - 1] = 'start';
        } else {
          session.foldWidgets[row - 1] = '';
        }

        if (indent < nextIndent) {
          return 'start';
        } else {
          return '';
        }
      };

    }).call(FoldMode.prototype);

  }
);

ace.define(
  'ace/mode/uncodercti',
  ['require', 'exports', 'module', 'ace/lib/oop', 'ace/mode/text', 'ace/mode/uncoder_cti_highlight_rules', 'ace/mode/matching_brace_outdent', 'ace/mode/folding/coffee'],
  function (require, exports) {
    'use strict';

    let oop = require('../lib/oop');
    let TextMode = require('./text').Mode;
    let UncoderCtiHighlightRules = require(
      './uncoder_cti_highlight_rules').UncoderCtiHighlightRules;
    let MatchingBraceOutdent = require(
      './matching_brace_outdent').MatchingBraceOutdent;
    let FoldMode = require('./folding/coffee').FoldMode;

    let Mode = function () {
      this.HighlightRules = UncoderCtiHighlightRules;
      this.$outdent = new MatchingBraceOutdent();
      this.foldingRules = new FoldMode();
      this.$behaviour = this.$defaultBehaviour;
    };
    oop.inherits(Mode, TextMode);

    (function () {

      this.lineCommentStart = ['#'];

      this.getNextLineIndent = function (state, line, tab) {
        let indent = this.$getIndent(line);

        if (state === 'start') {
          let match = line.match(/^.*[{(\[]\s*$/);
          if (match) {
            indent += tab;
          }
        }

        return indent;
      };

      this.checkOutdent = function (state, line, input) {
        return this.$outdent.checkOutdent(line, input);
      };

      this.autoOutdent = function (state, doc, row) {
        this.$outdent.autoOutdent(doc, row);
      };

      this.$id = 'ace/mode/uncodercti';
    }).call(Mode.prototype);

    exports.Mode = Mode;

  }
);

(function () {
  ace.require(['ace/mode/uncodercti'], function (m) {
    if (typeof module == 'object' && typeof exports == 'object' && module) {
      module.exports = m;
    }
  });
})();
