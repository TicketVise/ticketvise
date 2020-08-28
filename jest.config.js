module.exports = {
  verbose: true,
  roots: ["<rootDir>/frontend/components", "<rootDir>/frontend/tests"],
  moduleFileExtensions: ['js', 'vue'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/frontend/components/$1',
  },
  transform: {
    "^.+\\.js$": "babel-jest",
    "^.+\\.vue": "vue-jest",
  },
  snapshotSerializers: [
    "<rootDir>/node_modules/jest-serializer-vue"
  ]
}