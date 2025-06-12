const jsdoc = require('eslint-plugin-jsdoc');

module.exports = [
  {
    files: ['**/*.js'],
    languageOptions: {
      ecmaVersion: 2020,
      sourceType: 'script',
      globals: {
        gs: 'readonly',
        j2js: 'readonly',
        TableUtils: 'readonly'
      }
    },
    plugins: {
      jsdoc
    },
    settings: {
      jsdoc: {
        tagNamePreference: {
          'tag constructor': 'constructor'
        }
      }
    },
    rules: {
      'jsdoc/check-alignment': 'error',
      'jsdoc/check-param-names': 'error',
      'jsdoc/check-syntax': 'error',
      'jsdoc/check-tag-names': 'error',
      'jsdoc/check-types': 'error',
      'jsdoc/implements-on-classes': 'error',
      'jsdoc/no-undefined-types': 'error',
      'jsdoc/require-description': 'error',
      'jsdoc/require-param': 'error',
      'jsdoc/require-param-description': 'error',
      'jsdoc/require-param-name': 'error',
      'jsdoc/require-param-type': 'error',
      'jsdoc/require-returns': 'error',
      'jsdoc/require-returns-description': 'error',
      'jsdoc/require-returns-type': 'error',
      'jsdoc/valid-types': 'error'
    }
  }
];
