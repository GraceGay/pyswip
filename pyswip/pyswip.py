# pyswip.py

import sys

try:
	from ctypes import *
except ImportError:
	print>>sys.stderr, "A required module: 'ctypes' not found."
	sys.exit(1)
	
try:
	_lib = CDLL("libpl.so")
except OSError:
	print>>sys.stderr, "libpl (shared) not found. Possible reasons:"
	print>>sys.stderr, "1) SWI-Prolog not installed as a shared. Install SWI-Prolog (5.6.1)"
	print>>sys.stderr, "2) FIXME"
	sys.exit(1)
	
# constants (from SWI-Prolog.h)
PL_VARIABLE = 1  					# nothing 
PL_ATOM = 2  						# const char
PL_INTEGER = 3  # int
PL_FLOAT = 4  # double
#define PL_STRING	 (5)		/* const char * */
#define PL_TERM		 (6)

	#				/* PL_unify_term() */
#define PL_FUNCTOR	 (10)		/* functor_t, arg ... */
#define PL_LIST		 (11)		/* length, arg ... */
#define PL_CHARS	 (12)		/* const char * */
#define PL_POINTER	 (13)		/* void * */
	#				/* PlArg::PlArg(text, type) */
#define PL_CODE_LIST	 (14)		/* [ascii...] */
#define PL_CHAR_LIST	 (15)		/* [h,e,l,l,o] */
#define PL_BOOL		 (16)		/* PL_set_feature() */
#define PL_FUNCTOR_CHARS (17)		/* PL_unify_term() */
#define _PL_PREDICATE_INDICATOR (18)	/* predicate_t (Procedure) */
#define PL_SHORT	 (19)		/* short */
#define PL_INT		 (20)		/* int */
#define PL_LONG		 (21)		/* long */
#define PL_DOUBLE	 (22)		/* double */
#define PL_NCHARS	 (23)		/* unsigned, const char * */
#define PL_UTF8_CHARS	 (24)		/* const char * */
#define PL_UTF8_STRING	 (25)		/* const char * */
#define PL_INT64	 (26)		/* int64_t */
#define PL_NUTF8_CHARS	 (27)		/* unsigned, const char * */
#define PL_NUTF8_CODES	 (29)		/* unsigned, const char * */
#define PL_NUTF8_STRING	 (30)		/* unsigned, const char * */
#define PL_NWCHARS	 (31)		/* unsigned, const wchar_t * */
#define PL_NWCODES	 (32)		/* unsigned, const wchar_t * */
#define PL_NWSTRING	 (33)		/* unsigned, const wchar_t * */
#define PL_MBCHARS	 (34)		/* const char * */
#define PL_MBCODES	 (35)		/* const char * */
#define PL_MBSTRING	 (36)		/* const char * */

#		/********************************
#		* NON-DETERMINISTIC CALL/RETURN *
#		*********************************/
#
#  Note 1: Non-deterministic foreign functions may also use the deterministic
#    return methods PL_succeed and PL_fail.
#
#  Note 2: The argument to PL_retry is a 30 bits signed integer (long).

PL_FIRST_CALL = 0
PL_CUTTED = 1
PL_REDO = 2

PL_FA_NOTRACE = 0x01  # foreign cannot be traced
PL_FA_TRANSPARENT = 0x02  # foreign is module transparent
PL_FA_NONDETERMINISTIC	= 0x04  # foreign is non-deterministic
PL_FA_VARARGS = 0x08  # call using t0, ac, ctx
PL_FA_CREF = 0x10  # Internal: has clause-reference */

#		 /*******************************
#		 *	     CALL-BACK		*
#		 *******************************/

PL_Q_DEBUG = 0x01  # = TRUE for backward compatibility
PL_Q_NORMAL = 0x02  # normal usage
PL_Q_NODEBUG =  0x04  # use this one
PL_Q_CATCH_EXCEPTION = 0x08  # handle exceptions in C
PL_Q_PASS_EXCEPTION = 0x10  # pass to parent environment
PL_Q_DETERMINISTIC = 0x20  # call was deterministic

#		 /*******************************
#		 *	       BLOBS		*
#		 *******************************/

#define PL_BLOB_MAGIC_B	0x75293a00	/* Magic to validate a blob-type */
#define PL_BLOB_VERSION 1		/* Current version */
#define PL_BLOB_MAGIC	(PL_BLOB_MAGIC_B|PL_BLOB_VERSION)

#define PL_BLOB_UNIQUE	0x01		/* Blob content is unique */
#define PL_BLOB_TEXT	0x02		/* blob contains text */
#define PL_BLOB_NOCOPY	0x04		/* do not copy the data */
#define PL_BLOB_WCHAR	0x08		/* wide character string */

#		 /*******************************
#		 *	    CHAR BUFFERS	*
#		 *******************************/

CVT_ATOM = 0x0001
CVT_STRING = 0x0002
CVT_LIST = 0x0004
CVT_INTEGER	= 0x0008
CVT_FLOAT = 0x0010
CVT_VARIABLE = 0x0020
CVT_NUMBER = CVT_INTEGER | CVT_FLOAT
CVT_ATOMIC = CVT_NUMBER | CVT_ATOM | CVT_STRING
CVT_WRITE = 0x0040  # as of version 3.2.10
CVT_ALL = CVT_ATOMIC | CVT_LIST
CVT_MASK = 0x00ff

BUF_DISCARDABLE = 0x0000
BUF_RING = 0x0100
BUF_MALLOC = 0x0200

CVT_EXCEPTION = 0x10000  # throw exception on error
	
argv = (c_char_p*(len(sys.argv) + 1))()
for i, arg in enumerate(sys.argv):
	argv[i] = arg
	
argv[-1] = None
argc = len(sys.argv)

# types

atom_t = c_ulong
term_t = c_ulong
fid_t = c_ulong
module_t = c_void_p
predicate_t = c_void_p
record_t = c_void_p
qid_t = c_ulong
PL_fid_t = c_ulong
control_t = c_void_p
PL_engine_t = c_void_p
functor_t = c_ulong
PL_atomic_t = c_ulong
foreign_t = c_ulong
pl_wchar_t = c_wchar


##_lib.PL_initialise(len(sys.argv), _argv)

PL_initialise = _lib.PL_initialise
##PL_initialise.argtypes = [c_int, c_c

PL_open_foreign_frame = _lib.PL_open_foreign_frame
PL_open_foreign_frame.restype = fid_t

PL_new_term_ref = _lib.PL_new_term_ref
PL_new_term_ref.restype = term_t

PL_new_term_refs = _lib.PL_new_term_refs
PL_new_term_refs.restype = term_t

PL_chars_to_term = _lib.PL_chars_to_term
PL_chars_to_term.argtypes = [c_char_p, term_t]

PL_call = _lib.PL_call
PL_call.argtypes = [term_t, module_t]

PL_call_predicate = _lib.PL_call_predicate
PL_call_predicate.argtypes = [module_t, c_int, predicate_t, term_t]

PL_discard_foreign_frame = _lib.PL_discard_foreign_frame
PL_discard_foreign_frame.argtypes = [fid_t]

PL_put_list_chars = _lib.PL_put_list_chars
PL_put_list_chars.argtypes = [term_t, c_char_p]

PL_put_atom_chars = _lib.PL_put_atom_chars
PL_put_atom_chars.argtypes = [term_t, c_char_p]

PL_atom_chars = _lib.PL_atom_chars
PL_atom_chars.argtypes = [atom_t]
PL_atom_restype = [c_char_p]

PL_predicate = _lib.PL_predicate
PL_predicate.argtypes = [c_char_p, c_int, c_char_p]
PL_predicate.restype = predicate_t

PL_pred = _lib.PL_pred
PL_pred.argtypes = [functor_t, module_t]
PL_pred.restype = predicate_t

PL_open_query = _lib.PL_open_query
PL_open_query.argtypes = [module_t, c_int, predicate_t, term_t]
PL_open_query.restype = qid_t

PL_next_solution = _lib.PL_next_solution
PL_next_solution.argtypes = [qid_t]

PL_copy_term_ref = _lib.PL_copy_term_ref
PL_copy_term_ref.argtypes = [term_t]
PL_copy_term_ref.restype = term_t

PL_get_list = _lib.PL_get_list
PL_get_list.argtypes = [term_t, term_t, term_t]

PL_get_chars = _lib.PL_get_chars  # FIXME

PL_close_query = _lib.PL_close_query
PL_close_query.argtypes = [qid_t]

PL_halt = _lib.PL_halt
PL_halt.argtypes = [c_int]


def cstr2pystr(c_string):
	result = []
	for x in c_string:
		if x in ["\x00", None]:
			break
			
		result.append(x)
		
	return "".join(result)

def cstrarr2pystr(c_string):
	result = []
	for item in c_string:
		if item in ["\x00", None]:
			break
			
		r = []
		for x in item:
			if x in ["\x00", None]:
				break
			r.append(x)
		
		result.append("".join(r))
		
	return result
