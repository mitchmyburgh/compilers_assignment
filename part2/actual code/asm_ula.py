#----------------------------------------------
# run_ula.py
#
# runner for the ula (unconventional language)
# By Mitch Myburgh (MYBMIT001)
# 24 09 2015
#----------------------------------------------

#imports
import llvmlite.binding as llvm
import ir_ula
import os
import sys

# All these initializations are required for code generation!
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()  # yes, even this one

#generate the ir code and parse the machine code from it
module = str(ir_ula.run())
llvm_module = llvm.parse_assembly(str(module))
tm = llvm.Target.from_default_triple().create_target_machine()

# Compile the module to machine code using MCJIT
with llvm.create_mcjit_compiler(llvm_module, tm) as ee:
    ee.finalize_object()
    #print the output
    infilename = sys.argv[1]
    outfilename = os.path.splitext(infilename)[0]+".asm"
    outfile = open(outfilename, "w")
    print(tm.emit_assembly(llvm_module))
    print(tm.emit_assembly(llvm_module), file = outfile)
    outfile.close()
