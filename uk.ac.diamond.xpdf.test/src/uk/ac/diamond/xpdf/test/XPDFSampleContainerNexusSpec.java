package uk.ac.diamond.xpdf.test;

import java.util.Date;

import org.eclipse.dawnsci.nexus.NXbeam;
import org.eclipse.dawnsci.nexus.NXcontainer;
import org.eclipse.dawnsci.nexus.NXdata;
import org.eclipse.dawnsci.nexus.NXnote;
import org.eclipse.dawnsci.nexus.NXsample;
import org.eclipse.dawnsci.nexus.NexusNodeFactory;
import org.eclipse.january.dataset.Dataset;
import org.eclipse.january.dataset.DatasetFactory;
import org.eclipse.january.dataset.DoubleDataset;

public class XPDFSampleContainerNexusSpec {
	
	public static NXsample createContainerSample() {
		NXsample sample = NexusNodeFactory.createNXsample();
		
		sample.setNameScalar("empty 1mm capillary");
		sample.setDescriptionScalar("Empty Vitrex borosilicate 0.78 x 1 mm capillary");
		sample.addGroupNode("comments", NexusNodeFactory.createNXnote());//User notes - from DB?
		
		NXsample samComp1 = NexusNodeFactory.createNXsample(); //FIXME - should be NXsampleComponent!!
		samComp1.setNameScalar("borosilicate glass");
		samComp1.setChemical_formulaScalar("Si0.798 B0.221 Al0.023 Na0.066 K0.006O2");
		samComp1.setDensityScalar(2.23);
		samComp1.setAttribute("density", "units", "g cm-3");
		sample.addGroupNode("component_1", samComp1);
		
		NXbeam sampleBeam = NexusNodeFactory.createNXbeam();
		//TODO Needs thought
		
		sample.addGroupNode("beam", sampleBeam);
		
		return sample;
	}
	
	public static NXsample createSampleSample() {
		NXsample sample = NexusNodeFactory.createNXsample();
		
		sample.setNameScalar("TDBOX1");
		sample.setDescriptionScalar("An exciting double metal cyanide");
		NXnote comments = NexusNodeFactory.createNXnote();
		comments.setAuthorScalar("wnm24546");
		comments.setDateScalar(Date.from(XPDFTestUtils.getFakeNow().minusSeconds(60*60*72))); //Comment last updated 3 days earlier on iSPyB
		comments.setTypeScalar("test/plain");
		comments.setDataScalar("Sample was dehydrated at 130C for 12hrs under vacuum");
		sample.addGroupNode("comments", comments);
		
		NXsample samComp1 = NexusNodeFactory.createNXsample(); //FIXME - should be NXsampleComponent!!
		samComp1.setNameScalar("iron hexacyanocobaltate");
		samComp1.setChemical_formulaScalar("C6 N6 Fe Co");
		samComp1.setRelative_molecular_massScalar(286.413); //TODO should this be be chemical_formula_weight???
		samComp1.setDensityScalar(1.80);
		samComp1.setAttribute("density", "units", "g cm-3");
		samComp1.setUnit_cell_classScalar("cubic"); //Space group = Pm-3m; U/C a = 10.179
		samComp1.setUnit_cell_groupScalar("Pm-3m"); //TODO DAQ-619 - should be space group!
		samComp1.setUnit_cell(DatasetFactory.createFromObject(new double[]{10.179, 10.179, 10.179, 90., 90., 90.}, new int[]{2,3}));//TODO DAQ-619 - should be space group!
		String aa = "angstrom", oo = "degrees";
		samComp1.setAttribute("unit_cell", "units", DatasetFactory.createFromObject(new String[]{aa,aa,aa,oo,oo,oo}, new int[]{2,3}));
		samComp1.setUnit_cell_volumeScalar(1055.);
		samComp1.setAttribute("unit_cell_volume", "units", "angstrom3");
		samComp1.setField("crystal_structure", "Requires NeXus file spec!");//TODO Basham!
		
		sample.addGroupNode("component_1", samComp1);
		
		NXbeam sampleBeam = NexusNodeFactory.createNXbeam();
		//TODO Needs thought
		sample.addGroupNode("beam", sampleBeam);
		
		//Theoretical PDF
		NXdata pdfData = NexusNodeFactory.createNXdata();
		Dataset q = DatasetFactory.createRange(DoubleDataset.class, 0, 25.0, 0.01);
		Dataset trace = DatasetFactory.zeros(q);
		pdfData.setX(q);
		pdfData.setAttribute("x", "long_name", "Q");
		pdfData.setAttribute("x", "units", "angstrom-1"); // apparently, see units on NeXus website
		pdfData.setY(trace);
		pdfData.setAttribute(null, "signal", 1);
//		pdfData.setAttribute("data", "axes", ???); // symbolic link to x array
		sample.addGroupNode("theoretical_pdf", pdfData);
		
		return sample;
	}
	
	public static NXcontainer createContainerContainer() {
		NXcontainer cont = NexusNodeFactory.createNXcontainer();
		
		cont.setPacking_fractionScalar(1.);
		
		return cont;
	}

}
