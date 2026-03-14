#----------------------------------------------------------------
# Generated CMake target import file for configuration "Production".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "cvc5::cvc5parser" for configuration "Production"
set_property(TARGET cvc5::cvc5parser APPEND PROPERTY IMPORTED_CONFIGURATIONS PRODUCTION)
set_target_properties(cvc5::cvc5parser PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_PRODUCTION "cvc5::cvc5"
  IMPORTED_LOCATION_PRODUCTION "${_IMPORT_PREFIX}/lib/libcvc5parser.so.1"
  IMPORTED_SONAME_PRODUCTION "libcvc5parser.so.1"
  )

list(APPEND _IMPORT_CHECK_TARGETS cvc5::cvc5parser )
list(APPEND _IMPORT_CHECK_FILES_FOR_cvc5::cvc5parser "${_IMPORT_PREFIX}/lib/libcvc5parser.so.1" )

# Import target "cvc5::cvc5" for configuration "Production"
set_property(TARGET cvc5::cvc5 APPEND PROPERTY IMPORTED_CONFIGURATIONS PRODUCTION)
set_target_properties(cvc5::cvc5 PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_PRODUCTION "CLN;Poly;Polyxx;GMP"
  IMPORTED_LOCATION_PRODUCTION "${_IMPORT_PREFIX}/lib/libcvc5.so.1"
  IMPORTED_SONAME_PRODUCTION "libcvc5.so.1"
  )

list(APPEND _IMPORT_CHECK_TARGETS cvc5::cvc5 )
list(APPEND _IMPORT_CHECK_FILES_FOR_cvc5::cvc5 "${_IMPORT_PREFIX}/lib/libcvc5.so.1" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
