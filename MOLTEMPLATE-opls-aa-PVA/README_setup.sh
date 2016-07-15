# -------- REQUIREMENTS: ---------
#  You must define your MOLTEMPLATE_PATH environment variable
#  and set it to the "common" subdirectory of your moltemplate distribution.
#  (See the "Installation" section in the moltemplate manual.)

# Clean all the previous file
rm -rf -v system* moltemplate_files/*.lt moltemplate_files/*~ *~


# Create LAMMPS input files this way:
cd moltemplate_files

  # Build all the "*.lt" files
  rm -rf *.lt
  python write_polymer_moltemplate.py

  # Create the "oplsaa.lt" file which moltemplate will need
  cd oplsaa_lt_generator/
  oplsaa_moltemplate.py  oplsaa_subset.prm
  mv -f oplsaa.lt ..
  cd ..

  # run moltemplate
  moltemplate.sh system.lt

  # This will generate various files with names ending in *.in* and *.data. 
  # Move them to the directory where you plan to run LAMMPS (in this case "../")
  mv -f system.data system.in* ../

  # Optional:
  # The "./output_ttree/" directory is full of temporary files generated by 
  # moltemplate.  They can be useful for debugging, but are usually thrown away.
  rm -rf output_ttree/

  # Optional:
  # Delete the "oplsaa.lt" file:
  rm -f oplsaa.lt
  
cd ../

# Apply atactic condition
python apply_atacticity.py

# Rewrite the data file using Moltemplate
python rewrite-datalammps-topotools.py
