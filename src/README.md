Polonator Processor software,
David Kalish,
12/14/2010,

EXECUTE FILE:
        PolProcPy_034.py    (stable),
        PolProcPy_035.py    (unstable)

LIST OF FILES:
        analyze_reads.py,
        autoQC.py,
        basecall.py,
        commify.py,
        compile.py,
        create_tarball.py,
        disp_delta.py,
        disp_regQC.py,
        disp_tetra.py,
        disp_tetra-delta.py,
        find_running_processes.py,
        histogram.py,
        histogram4.py,
        homopolymer_accuracy.py,
        initialize_processor.py,
        makePrimerFile.py,
        PolProcPy_03x.py (030, 031, 032, 033, 034, and 035),
        process_kill.py,
        process_tools.py,
        processor.py,
        pull_regcoords.py,
        pull_regpoints.py,
        pull_segpoints.py,
        qc_reg.py,
        summarize_beadsums.py,
        summarize_init.py,
        ui_polonatorprocessor_03.py,

MAKE SURE:
        Make sure compile.py is located in the src folder in project.

IF A PYTHON FILE DOESN'T WORK IN THE GUI:
        Find the Perl file with the same name and copy it into your
        working directory.  In the PolProcPy_03x.py file, search for 
        "python (filename).py" and change it to "perl (filename).pl"