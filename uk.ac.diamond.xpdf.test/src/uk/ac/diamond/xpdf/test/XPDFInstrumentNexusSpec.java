package uk.ac.diamond.xpdf.test;

import java.util.Date;

import org.eclipse.dawnsci.analysis.api.tree.DataNode;
import org.eclipse.dawnsci.nexus.NXaperture;
import org.eclipse.dawnsci.nexus.NXattenuator;
import org.eclipse.dawnsci.nexus.NXbeam;
import org.eclipse.dawnsci.nexus.NXcollection;
import org.eclipse.dawnsci.nexus.NXcrystal;
import org.eclipse.dawnsci.nexus.NXdetector;
import org.eclipse.dawnsci.nexus.NXinsertion_device;
import org.eclipse.dawnsci.nexus.NXinstrument;
import org.eclipse.dawnsci.nexus.NXlog;
import org.eclipse.dawnsci.nexus.NXmirror;
import org.eclipse.dawnsci.nexus.NXmonitor;
import org.eclipse.dawnsci.nexus.NXmonochromator;
import org.eclipse.dawnsci.nexus.NXnote;
import org.eclipse.dawnsci.nexus.NXpositioner;
import org.eclipse.dawnsci.nexus.NXslit;
import org.eclipse.dawnsci.nexus.NXsource;
import org.eclipse.dawnsci.nexus.NexusNodeFactory;
import org.eclipse.january.dataset.DatasetFactory;
import org.eclipse.january.dataset.DoubleDataset;

public final class XPDFInstrumentNexusSpec {
	
	public static void populateNXinstrument(NXinstrument instrument, long durationSecs) {
		//Set names
		instrument.setNameScalar("i15-1");
		instrument.setField("alt_name", "XPDF");
		
		//Add non-default beamline devices
		//Source
		//Insertion device
		instrument.addGroupNode("primary_slit", NexusNodeFactory.createNXslit());
		instrument.addGroupNode("filter_1", NexusNodeFactory.createNXattenuator());
		instrument.addGroupNode("filter_2", NexusNodeFactory.createNXattenuator());
		instrument.addGroupNode("filter_3", NexusNodeFactory.createNXattenuator());
		instrument.setMonochromator("bent_laue_monochromator", NexusNodeFactory.createNXmonochromator());
		instrument.addGroupNode("beam_position_monitor_1", NexusNodeFactory.createNXmonitor());
		instrument.addGroupNode("secondary_slit", NexusNodeFactory.createNXslit());
		instrument.addGroupNode("multi_layer_mirror", NexusNodeFactory.createNXmirror());
		instrument.addGroupNode("optical_rail", NexusNodeFactory.createNXcollection()); //TODO NXstage!
		instrument.addGroupNode("beam_defining_aperture", NexusNodeFactory.createNXslit());
		instrument.addGroupNode("beam_position_monitor_2", NexusNodeFactory.createNXmonitor());
		instrument.addGroupNode("first_sample_slit", NexusNodeFactory.createNXslit());
		instrument.addGroupNode("second_sample_slit", NexusNodeFactory.createNXslit());
		instrument.addGroupNode("i0_beam_position_monitor_3", NexusNodeFactory.createNXmonitor());
		instrument.addGroupNode("cleanup", NexusNodeFactory.createNXaperture());
		instrument.addGroupNode("sample_stage", NexusNodeFactory.createNXcollection()); //TODO NXstage
		instrument.addGroupNode("detector_1", NexusNodeFactory.createNXdetector());
		instrument.addGroupNode("detector_2", NexusNodeFactory.createNXdetector());
		
		/*
		 * Source
		 */
		NXsource source = NexusNodeFactory.createNXsource();
		source.setNameScalar("Diamond Light Source");
		source.setTypeScalar("Synchrotron X-ray Source");
		source.setProbeScalar("x-ray");
		source.setEnergyScalar(3.0);
		source.setAttribute("energy", "units", "GeV");
		source.setCurrent(DatasetFactory.createLinearSpace(DoubleDataset.class, 301.1, 295.5, (int)durationSecs));
		source.setAttribute("current", "description", "Variation of ring current over the course of the experiment");
//		source.setTop_upScalar(new Boolean(false)); //FIXME (DAQ-614)
		source.setLast_fillScalar(301.2);
		source.setLast_fillAttributeTime(Date.from(XPDFTestUtils.getFakeNow().minusSeconds(487)));
		source.setField("machine_status_message_1", "User beam");//TODO Question for Basham: could this be done as a Dataset of Strings (e.g. a list?)
		source.setField("machine_status_message_2", "Low alpha mode");
		source.setDistanceScalar(-35.5);
		source.setAttribute("distance", "units", "m");
		instrument.setSource(source);
		
		/*
		 * Insertion Device
		 */
		NXinsertion_device idev = NexusNodeFactory.createNXinsertion_device();
		idev.setTypeScalar("wiggler");
		idev.setGapScalar(60.);
		idev.setAttribute("gap", "units", "mm");
		idev.setLengthScalar(1.44);
		idev.setAttribute("length", "units", "m");
		//TODO Question for Basham: there's no option for field here.
		instrument.setInsertion_device(idev);
		
		/*
		 * Primary slit
		 */
		populatePrimarySlit(instrument);
		
		/*
		 * Attenuator 1
		 */
		NXattenuator filter1 = instrument.getChild("filter_1", NXattenuator.class);
		filter1.setTypeScalar("Diamond");
		filter1.setThicknessScalar(1.2);
		filter1.setAttenuator_transmissionScalar(0.2);
		filter1.setStatusScalar("2"); //which position is it at
		NXpositioner filter1Motor = NexusNodeFactory.createNXpositioner();
		filter1Motor.setNameScalar("att1Y");
		filter1Motor.setDescriptionScalar("Filter 1 position");
		filter1Motor.setValueScalar(1.5);
		filter1Motor.setAttribute("value", "units", "mm");
		filter1.addGroupNode("filter_1_motor", filter1Motor);
		filter1.setAttribute("filter_1_motor", "controller_record", "EPICS::att1Y");
		filter1.setDistanceScalar(-10.5);
		filter1.setAttribute("distance", "units", "m");
		
		/*
		 * Attenuator 2
		 */
		NXattenuator filter2 = instrument.getChild("filter_2", NXattenuator.class);
		filter2.setTypeScalar("Silicon Carbide");
		filter2.setThicknessScalar(4.0);
		filter2.setAttenuator_transmissionScalar(0.5);
		filter2.setStatusScalar("1"); //which position is it at
		NXpositioner filter2Motor = NexusNodeFactory.createNXpositioner();
		filter2Motor.setNameScalar("att2Y");
		filter2Motor.setDescriptionScalar("Filter 2 position");
		filter2Motor.setValueScalar(1.5);
		filter2Motor.setAttribute("value", "units", "mm");
		filter2.addGroupNode("filter_2_motor", filter2Motor);
		filter2.setAttribute("filter_2_motor", "controller_record", "EPICS::att2Y");
		filter2.setDistanceScalar(-10.5);
		filter2.setAttribute("distance", "units", "m");
		
		/*
		 * Attenuator 3
		 */
		NXattenuator filter3 = instrument.getChild("filter_3", NXattenuator.class);
		filter3.setTypeScalar("Silicon Carbide");
		filter3.setThicknessScalar(1.0);
		filter3.setAttenuator_transmissionScalar(0.1);
		filter3.setStatusScalar("1"); //which position is it at
		NXpositioner filter3Motor = NexusNodeFactory.createNXpositioner();
		filter3Motor.setNameScalar("att3Y");
		filter3Motor.setDescriptionScalar("Filter 3 position");
		filter3Motor.setValueScalar(1.5);
		filter3Motor.setAttribute("value", "units", "mm");
		filter3.addGroupNode("filter_3_motor", filter3Motor);
		filter3.setAttribute("filter_3_motor", "controller_record", "EPICS::att3Y");
		filter3.setDistanceScalar(-10.5);
		filter3.setAttribute("distance", "units", "m");
		
		/*
		 * Monochromator
		 */
		populateBLM(instrument);
		
		/*
		 * BPM1
		 */
		NXmonitor bpm1 = instrument.getChild("beam_position_monitor_1", NXmonitor.class);
		bpm1.setField("description", "YAG:Ce screen with camera");
		bpm1.setTypeScalar("Fluorescent screen");
		//TODO Do we want any data here? e.g. data, count_time, x/y_centre, x/y_size 
		bpm1.setField("status", "out");
		bpm1.setDistanceScalar(-15.); //This is made up
		bpm1.setAttribute("distance", "units", "m");
		
		/*
		 * Secondary slit
		 */
		populateSecondarySlit(instrument);
		
		/*
		 * Multilayer mirror
		 */
		populateMultilayerMirror(instrument);
		
		/*
		 * Optical rail
		 */
		NXcollection opticalRail = instrument.getChild("optical_rail", NXcollection.class);//NXstage
		opticalRail.addGroupNode("transforms", NexusNodeFactory.createNXtransformations());//TODO Basham
		
		NXcollection railMotors = NexusNodeFactory.createNXcollection();
		NXpositioner railYMotor = NexusNodeFactory.createNXpositioner();
		railYMotor.setNameScalar("railusY");
		railYMotor.setDescriptionScalar("Rail upstream Y motor");
		railYMotor.setValueScalar(1.5);
		railYMotor.setAttribute("value", "units", "mm");
		railMotors.addGroupNode("upstream_y", railYMotor);
		railMotors.setAttribute("upstream_y", "controller_record", "EPICS::railusY");
		NXpositioner railXMotor = NexusNodeFactory.createNXpositioner();
		railXMotor.setNameScalar("railusX");
		railXMotor.setDescriptionScalar("Rail upstream X motor");
		railXMotor.setValueScalar(1.5);
		railXMotor.setAttribute("value", "units", "mm");
		railMotors.addGroupNode("upstream_x", railYMotor);
		railMotors.setAttribute("upstream_x", "controller_record", "EPICS::railusX");
		opticalRail.addGroupNode("motors", railMotors);
		
		/*
		 * Beam defining aperture
		 */
		populateBeamDefiningAperture(instrument);
		
		/*
		 * BPM 2
		 */
		NXmonitor bpm2 = instrument.getChild("beam_position_monitor_2", NXmonitor.class);
		bpm2.setField("description", "YAG:Ce screen with camera");
		bpm2.setTypeScalar("Fluorescent screen");
		//TODO Do we want any data here? e.g. data, count_time, x/y_centre, x/y_size 
		bpm2.setField("status", "out");
		bpm2.setDistanceScalar(-5.); //This is made up
		bpm2.setAttribute("distance", "units", "m");
		
		/*
		 * 1st sample slit
		 */
		populateFirstSampleSlit(instrument);
		
		/*
		 * 2nd sample slit
		 */
		populateSecondSampleSlit(instrument);
		
		/*
		 * I0 BPM 3
		 */
		populateI0Monitor(instrument, durationSecs);
		
		/*
		 * Cleanup
		 */
		NXaperture cleanup = instrument.getChild("cleanup", NXaperture.class);
		cleanup.setMaterialScalar("Gold");
		cleanup.setDescriptionScalar("Gold clean-up aperture");
		cleanup.addGroupNode("transforms", NexusNodeFactory.createNXtransformations());//TODO Basham
		
		NXcollection cleanupMotors = NexusNodeFactory.createNXcollection();
		NXpositioner cleanX = NexusNodeFactory.createNXpositioner();
		cleanX.setNameScalar("cleanX");
		cleanX.setDescriptionScalar("Aperture X position");
		cleanX.setValueScalar(1.7);
		cleanX.setAttribute("value", "units", "mm");
		cleanupMotors.addGroupNode("clean_x", cleanX);
		cleanupMotors.setAttribute("clean_x", "controller_record", "EPICS::cleanX");
		NXpositioner cleanY = NexusNodeFactory.createNXpositioner();
		cleanY.setNameScalar("cleanY");
		cleanY.setDescriptionScalar("Aperture X position");
		cleanY.setValueScalar(1.5);
		cleanY.setAttribute("value", "units", "mm");
		cleanupMotors.addGroupNode("clean_y", cleanY);
		cleanupMotors.setAttribute("clean_y", "controller_record", "EPICS::cleanY");
		cleanup.addGroupNode("motors", cleanupMotors);
		
		/*
		 * Sample stage
		 */
		NXcollection sampleStage = instrument.getChild("sample_stage", NXcollection.class);//TODO NXstage. This is a prototype version really!
		sampleStage.setField("sample_changer_position", 4);
		sampleStage.setField("sample_changer_capacity", 10);
		NXpositioner sampleX = NexusNodeFactory.createNXpositioner();
		sampleX.setNameScalar("samX");
		sampleX.setDescriptionScalar("Stage X position");
		sampleX.setValueScalar(20.18);
		sampleX.setAttribute("value", "units", "mm");
		sampleStage.addGroupNode("sample_x", sampleX);
		sampleStage.setAttribute("sample_x", "controller_record", "EPICS::samX");
		NXpositioner sampleY = NexusNodeFactory.createNXpositioner();
		sampleY.setNameScalar("samY");
		sampleY.setDescriptionScalar("Stage Y position");
		sampleY.setValueScalar(180.58);
		sampleY.setAttribute("value", "units", "mm");
		sampleStage.addGroupNode("sample_y", sampleY);
		sampleStage.setAttribute("sample_y", "controller_record", "EPICS::samY");
		sampleStage.addGroupNode("transforms", NexusNodeFactory.createNXtransformations());//TODO Basham
		
		/*
		 * Detectors
		 */
		populateDetector1(instrument, durationSecs);
		populateDetector2(instrument, durationSecs);

	}
	
	/*********************************************************************
	 * Below here are complex devices
	 * *******************************************************************
	 */

	private static void populatePrimarySlit(NXinstrument instrument) {
		NXslit priSlit = instrument.getChild("primary_slit", NXslit.class);
		
		/*
		 * Primary slits
		 */
		priSlit.setX_gapScalar(1.2);
		priSlit.setAttribute("x_gap", "units", "mm");
		priSlit.setAttribute("x_gap", "local_name", "s1gapX");
		priSlit.setAttribute("x_gap", "controller_record", "EPICS::s1gapX");
		priSlit.setY_gapScalar(2.21);
		priSlit.setAttribute("y_gap", "units", "mm");
		priSlit.setAttribute("y_gap", "local_name", "s1gapY");
		priSlit.setAttribute("y_gap", "controller_record", "EPICS::s1gapY");
		priSlit.addGroupNode("transforms", NexusNodeFactory.createNXtransformations());//TODO Basham
		
		NXbeam priSlitBeam = NexusNodeFactory.createNXbeam();
		priSlitBeam.setIncident_beam_divergence(DatasetFactory.createFromObject(new double[]{0.4, 0.98}, new int[]{2})); //TODO Numbers will be needed from Phil
		priSlitBeam.setAttribute("incident_beam_divergence", "units", "radians");
		priSlitBeam.setFinal_beam_divergence(DatasetFactory.createFromObject(new double[]{0.3, 0.7}, new int[]{2})); //TODO Numbers will be needed from Phil
		priSlitBeam.setAttribute("final_beam_divergence", "units", "radians");
		priSlit.addGroupNode("beam", priSlitBeam);

		NXcollection priSlitMotors = NexusNodeFactory.createNXcollection(); //TODO NXstage
		NXpositioner dsX = NexusNodeFactory.createNXpositioner();
		dsX.setNameScalar("s1dsX");
		dsX.setDescriptionScalar("Downstream X motor");
		dsX.setValueScalar(1.258);
		dsX.setAttribute("value", "units", "mm");
		priSlitMotors.addGroupNode("downstream_x", dsX);
		priSlitMotors.setAttribute("downstream_x", "controller_record", "EPICS::s1dsX");
		NXpositioner dsY = NexusNodeFactory.createNXpositioner();
		dsY.setNameScalar("s1dsY");
		dsY.setDescriptionScalar("Downstream Y motor");
		dsY.setValueScalar(3.25);
		dsY.setAttribute("value", "units", "mm");
		priSlitMotors.addGroupNode("downstream_y", dsY);
		priSlitMotors.setAttribute("downstream_y", "controller_record", "EPICS::s1dsY");
		NXpositioner usX = NexusNodeFactory.createNXpositioner();
		usX.setNameScalar("s1usX");
		usX.setDescriptionScalar("Upstream X motor");
		usX.setValueScalar(1.258);
		usX.setAttribute("value", "units", "mm");
		priSlitMotors.addGroupNode("upstream_x", usX);
		priSlitMotors.setAttribute("upstream_x", "controller_record", "EPICS::s1usX");
		NXpositioner usY = NexusNodeFactory.createNXpositioner();
		usY.setNameScalar("s1usY");
		usY.setDescriptionScalar("Upstream Y motor");
		usY.setValueScalar(1.258);
		usY.setAttribute("value", "units", "mm");
		priSlitMotors.addGroupNode("upstream_y", usY);
		priSlitMotors.setAttribute("upstream_y", "controller_record", "EPICS::s1usy");
		priSlit.addGroupNode("motors", priSlitMotors);
	}
	
	private static void populateBLM(NXinstrument instrument) {
		NXmonochromator blm = instrument.getChild("bent_laue_monochromator", NXmonochromator.class);
		blm.setWavelengthScalar(0.161669);
		blm.setAttribute("wavelength", "units", "angstrom");
		blm.setAttribute("wavelength", "local_name", "xtalWavelength");
		blm.setAttribute("wavelength", "controller_record", "EPICS::xtalWavelength");
		blm.setEnergyScalar(76.69);
		blm.setAttribute("energy", "units", "keV");
		blm.setAttribute("energy", "local_name", "xtalEnergy");
		blm.setAttribute("energy", "controller_record", "EPICS::xtalEnergy");
		blm.setField("bandwidth", 0.2);
		
		NXcrystal xtal = NexusNodeFactory.createNXcrystal();
		xtal.setUsageScalar("Laue");
		xtal.setTypeScalar("Si");
		xtal.setReflection(DatasetFactory.createFromObject(new Integer[]{3,1,1}, new int[]{3}));
		xtal.setCurvature_horizontalScalar(2.);
		xtal.setAttribute("curvature_horizontal", "units", "mm");
		xtal.setAttribute("curvature_horizontal", "description", "Horizontal radius of curvature");
		xtal.setThicknessScalar(3.0);
		xtal.setAttribute("thickness", "units", "mm");
		xtal.setCut_angleScalar(-2.61);
		xtal.setAttribute("cut_angle", "units", "degrees");
//		xtal.setIs_cylindricalScalar(true); //FIXME DAQ-614
		NXlog xtalTempLog = NexusNodeFactory.createNXlog();
		xtalTempLog.setDescriptionScalar("Temperature of monochromator crystal");
		//TODO Put stuff in here??
		xtal.setTemperature_log(xtalTempLog);
		xtal.setField("focal_length", 20.0);
		xtal.setAttribute("focal_length", "units", "mm");
		xtal.setAttribute("focal_length", "local_name", "xtalFocus");
		xtal.setAttribute("focal_length", "controller_record", "EPICS::xtalFocus");
		blm.setCrystal(xtal);
		
		NXbeam monoBeam = NexusNodeFactory.createNXbeam();
		monoBeam.setIncident_wavelength_spreadScalar(0.24);
		monoBeam.setAttribute("incident_wavelength_spread", "units", "angstrom");
		monoBeam.setFinal_wavelength_spreadScalar(0.001);
		monoBeam.setAttribute("final_wavelength_spread", "units", "angstrom");
		monoBeam.addSymbolicNode("incident_beam_divergence", NexusNodeFactory.createSymbolicNode(XPDFTestUtils.getNexusTree().getSourceURI(), "/entry1/instrument/primary_slit/beam/final_beam_divergence"));
		monoBeam.setFinal_beam_divergence(DatasetFactory.createFromObject(new double[]{0.25, 0.61}, new int[]{2})); //TODO Numbers will be needed from Phil)
		monoBeam.setAttribute("final_beam_divergence", "units", "radians");
		blm.addGroupNode("beam", monoBeam);
		
		blm.addGroupNode("transforms", NexusNodeFactory.createNXtransformations());//TODO Basham
		
		NXcollection blmMotors = NexusNodeFactory.createNXcollection(); //TODO NXstage
		NXpositioner pitch = NexusNodeFactory.createNXpositioner();
		pitch.setNameScalar("xtalBragg");
		pitch.setDescriptionScalar("Pitch of crystal cage");
		pitch.setValueScalar(1.258);
		pitch.setAttribute("value", "units", "degrees");
		blmMotors.addGroupNode("pitch", pitch);
		blmMotors.setAttribute("pitch", "controller_record", "EPICS::xtalBragg");
		NXpositioner finePitch = NexusNodeFactory.createNXpositioner();
		finePitch.setNameScalar("xtalFine");
		finePitch.setDescriptionScalar("Fine pitch of crystal cage");
		finePitch.setValueScalar(3.25);
		finePitch.setAttribute("value", "units", "degrees");
		blmMotors.addGroupNode("pitch_fine", finePitch);
		blmMotors.setAttribute("pitch_fine", "controller_record", "EPICS::xtalFine");
		NXpositioner yaw = NexusNodeFactory.createNXpositioner();
		yaw.setNameScalar("xtalYaw");
		yaw.setDescriptionScalar("Yaw of crystal cage");
		yaw.setValueScalar(1.7);
		yaw.setAttribute("value", "units", "degrees");
		blmMotors.addGroupNode("yaw", yaw);
		blmMotors.setAttribute("yaw", "controller_record", "EPICS::xtalYaw");
		NXpositioner roll = NexusNodeFactory.createNXpositioner();
		roll.setNameScalar("xtalRoll");
		roll.setDescriptionScalar("Roll of crystal cage");
		roll.setValueScalar(1.5);
		roll.setAttribute("value", "units", "degrees");
		blmMotors.addGroupNode("roll", roll);
		blmMotors.setAttribute("roll", "controller_record", "EPICS::xtalRoll");
		NXpositioner yPosition = NexusNodeFactory.createNXpositioner();
		yPosition.setNameScalar("xtalY");
		yPosition.setDescriptionScalar("Vertical translation of crystal cage");
		yPosition.setValueScalar(1.5);
		yPosition.setAttribute("value", "units", "mm");
		blmMotors.addGroupNode("y_position", yPosition);
		blmMotors.setAttribute("y_position", "controller_record", "EPICS::xtalY");
		NXpositioner bender = NexusNodeFactory.createNXpositioner();
		bender.setNameScalar("xtalBend");
		bender.setDescriptionScalar("Crystal bender actuator");
		bender.setValueScalar(1.5);
		bender.setAttribute("value", "units", "mm");
		blmMotors.addGroupNode("bender", bender);
		blmMotors.setAttribute("bender", "controller_record", "EPICS::xtalBend");
		blm.addGroupNode("motors", blmMotors);
	}
	
	private static void populateSecondarySlit(NXinstrument instrument) {
		NXslit secSlit = instrument.getChild("secondary_slit", NXslit.class);
		
		/*
		 * Secondary slits
		 */
		secSlit.setX_gapScalar(1.8);
		secSlit.setAttribute("x_gap", "units", "mm");
		secSlit.setAttribute("x_gap", "local_name", "s2gapX");
		secSlit.setAttribute("x_gap", "controller_record", "EPICS::s2gapX");
		secSlit.setY_gapScalar(1.9);
		secSlit.setAttribute("y_gap", "units", "mm");
		secSlit.setAttribute("y_gap", "local_name", "s2gapY");
		secSlit.setAttribute("y_gap", "controller_record", "EPICS::s2gapY");
		secSlit.addGroupNode("transforms", NexusNodeFactory.createNXtransformations());//TODO Basham
		
		NXbeam secSlitBeam = NexusNodeFactory.createNXbeam();
		secSlitBeam.addSymbolicNode("incident_wavelength_spread", NexusNodeFactory.createSymbolicNode(XPDFTestUtils.getNexusTree().getSourceURI(), "/entry1/instrument/bent_laue_monochromator/beam/final_wavelength_spread"));
		secSlitBeam.setFinal_wavelength_spreadScalar(0.0008);
		secSlit.addSymbolicNode("incident_beam_divergence", NexusNodeFactory.createSymbolicNode(XPDFTestUtils.getNexusTree().getSourceURI(), "/entry1/instrument/bent_laue_monochromator/beam/final_beam_divergence"));
		secSlitBeam.setFinal_beam_divergence(DatasetFactory.createFromObject(new double[]{0.3, 0.68}, new int[]{2})); //TODO Numbers will be needed from Phil
		secSlitBeam.setAttribute("final_beam_divergence", "units", "radians");
		secSlit.addGroupNode("beam", secSlitBeam);

		NXcollection secSlitMotors = NexusNodeFactory.createNXcollection(); //TODO NXstage
		NXpositioner leftSlit = NexusNodeFactory.createNXpositioner();
		leftSlit.setNameScalar("s2obxX");
		leftSlit.setDescriptionScalar("Outboard slit X motor");
		leftSlit.setValueScalar(1.258);
		leftSlit.setAttribute("value", "units", "mm");
		secSlitMotors.addGroupNode("left_slit", leftSlit);
		secSlitMotors.setAttribute("left_slit", "controller_record", "EPICS::s2obx");
		NXpositioner rightSlit = NexusNodeFactory.createNXpositioner();
		rightSlit.setNameScalar("s2ibx");
		rightSlit.setDescriptionScalar("Inboard slit X motor");
		rightSlit.setValueScalar(3.25);
		rightSlit.setAttribute("value", "units", "mm");
		secSlitMotors.addGroupNode("right_slit", rightSlit);
		secSlitMotors.setAttribute("right_slit", "controller_record", "EPICS::s2ibx");
		NXpositioner topSlit = NexusNodeFactory.createNXpositioner();
		topSlit.setNameScalar("s2topY");
		topSlit.setDescriptionScalar("Top slit Y motor");
		topSlit.setValueScalar(1.258);
		topSlit.setAttribute("value", "units", "mm");
		secSlitMotors.addGroupNode("top_slit", topSlit);
		secSlitMotors.setAttribute("top_slit", "controller_record", "EPICS::s2topy");
		NXpositioner bottomSlit = NexusNodeFactory.createNXpositioner();
		bottomSlit.setNameScalar("s2botY");
		bottomSlit.setDescriptionScalar("Bottom slit Y motor");
		bottomSlit.setValueScalar(1.258);
		bottomSlit.setAttribute("value", "units", "mm");
		secSlitMotors.addGroupNode("bottom_slit", bottomSlit);
		secSlitMotors.setAttribute("bottom_slit", "controller_record", "EPICS::s2boty");
		secSlit.addGroupNode("motors", secSlitMotors);
	}
	
	private static void populateMultilayerMirror(NXinstrument instrument) {
		NXmirror mlm = instrument.getChild("multi_layer_mirror", NXmirror.class);
		
		/*
		 * Multilayer mirror
		 */
		mlm.setTypeScalar("multi");
		mlm.setDescriptionScalar("Elliptically shaped multi-layer coated bimorph mirror");
		mlm.setField("focal_length", 20.0);
		mlm.setAttribute("focal_length", "units", "mm");
		mlm.setAttribute("focal_length", "local_name", "m1Focus");
		mlm.setAttribute("focal_length", "controller_record", "EPICS::m1Focus");
		mlm.setIncident_angleScalar(0.0042);
		mlm.setAttribute("incident_angle", "units", "radians");
		mlm.setShape(NexusNodeFactory.createNXshape());//TODO Basham
		DataNode dn = NexusNodeFactory.createDataNode();
		dn.setDataset(DatasetFactory.createFromObject(new Double[]{20., 12.5, 0.54, 0.058, 0.85, 0.796, 25.58, 12.6,
																   4.6, 5.57, 0.08, 0.587, 7.56, 6.518, 3.586, 1.58}, new int[]{16}));
		mlm.addDataNode("bend_voltages", dn);
		mlm.setInterior_atmosphereScalar("vacuum");
		NXlog xtalTempLog = NexusNodeFactory.createNXlog();
		xtalTempLog.setDescriptionScalar("Temperature of mirror");
		//TODO Put stuff in here??
		mlm.addGroupNode("temperature_log", xtalTempLog);
		mlm.setSubstrate_materialScalar("Si");
		mlm.setSubstrate_densityScalar(2.330);
		mlm.setAttribute("substrate_density", "units", "g cm-3");
		mlm.setEven_layer_materialScalar("B4C");
		mlm.setEven_layer_densityScalar(2.503);
		mlm.setAttribute("even_layer_density", "units", "g cm-3");
		mlm.setAttribute("even_layer_density", "note", "Actual density >85% of this value");
		mlm.setOdd_layer_materialScalar("Ni");
		mlm.setOdd_layer_densityScalar(8.908);
		mlm.setAttribute("odd_layer_density", "units", "g cm-3");
		mlm.setAttribute("odd_layer_density", "note", "Actual density >85% of this value");
		mlm.setLayer_thicknessScalar(38.34);
		mlm.setAttribute("layer_thickness", "note", "Inter-layer separation at centre of mirror");
		mlm.addGroupNode("transforms", NexusNodeFactory.createNXtransformations());//TODO Basham
		
		NXbeam mlmBeam = NexusNodeFactory.createNXbeam();
		mlmBeam.addSymbolicNode("incident_wavelength_spread", NexusNodeFactory.createSymbolicNode(XPDFTestUtils.getNexusTree().getSourceURI(), "/entry1/instrument/secondary_slit/beam/final_wavelength_spread"));
		mlmBeam.setFinal_wavelength_spreadScalar(0.0008);
		mlmBeam.addSymbolicNode("incident_beam_divergence", NexusNodeFactory.createSymbolicNode(XPDFTestUtils.getNexusTree().getSourceURI(), "/entry1/instrument/secondary_slit/beam/final_beam_divergence"));
		mlmBeam.setFinal_beam_divergence(DatasetFactory.createFromObject(new double[]{0.21, 0.57}, new int[]{2})); //TODO Numbers will be needed from Phil
		mlmBeam.setAttribute("final_beam_divergence", "units", "radians");
		
		NXcollection mlmMotors = NexusNodeFactory.createNXcollection(); //TODO NXstage
		NXpositioner upstreamX = NexusNodeFactory.createNXpositioner();
		upstreamX.setNameScalar("m1usX");
		upstreamX.setDescriptionScalar("MLM upstream X motor");
		upstreamX.setValueScalar(1.258);
		upstreamX.setAttribute("value", "units", "mm");
		mlmMotors.addGroupNode("upstream_X", upstreamX);
		mlmMotors.setAttribute("upstream_X", "controller_record", "EPICS::m1usX");
		NXpositioner downstreamX = NexusNodeFactory.createNXpositioner();
		downstreamX.setNameScalar("m1dsX");
		downstreamX.setDescriptionScalar("MLM downstream X motor");
		downstreamX.setValueScalar(3.25);
		downstreamX.setAttribute("value", "units", "mm");
		mlmMotors.addGroupNode("downstream_X", downstreamX);
		mlmMotors.setAttribute("downstream_X", "controller_record", "EPICS::m1dsX");
		NXpositioner upstreamInboardY = NexusNodeFactory.createNXpositioner();
		upstreamInboardY.setNameScalar("m1ibY");
		upstreamInboardY.setDescriptionScalar("MLM inboard upstream Y motor");
		upstreamInboardY.setValueScalar(1.7);
		upstreamInboardY.setAttribute("value", "units", "mm");
		mlmMotors.addGroupNode("upstream_inboard_y", upstreamInboardY);
		mlmMotors.setAttribute("upstream_inboard_y", "controller_record", "EPICS::m1ibY");
		NXpositioner upstreamOutboardY = NexusNodeFactory.createNXpositioner();
		upstreamOutboardY.setNameScalar("m1obY");
		upstreamOutboardY.setDescriptionScalar("MLM outboard upstream Y motor");
		upstreamOutboardY.setValueScalar(1.5);
		upstreamOutboardY.setAttribute("value", "units", "mm");
		mlmMotors.addGroupNode("upstream_outboard_y", upstreamOutboardY);
		mlmMotors.setAttribute("upstream_outboard_y", "upstream_outboard_y", "EPICS::m1obY");
		NXpositioner downstreamY = NexusNodeFactory.createNXpositioner();
		downstreamY.setNameScalar("m1dsY");
		downstreamY.setDescriptionScalar("MLM downstream Y motor");
		downstreamY.setValueScalar(1.5);
		downstreamY.setAttribute("value", "units", "mm");
		mlmMotors.addGroupNode("downstream_Y", downstreamY);
		mlmMotors.setAttribute("downstream_Y", "controller_record", "EPICS::m1dsY");
		mlm.addGroupNode("motors", mlmMotors);
	}

	private static void populateBeamDefiningAperture(NXinstrument instrument) {
		NXslit beamDefAp = instrument.getChild("beam_defining_aperture", NXslit.class);
		
		/*
		 * Beam defining slits
		 */
		beamDefAp.setX_gapScalar(1.7);
		beamDefAp.setAttribute("x_gap", "units", "mm");
		beamDefAp.setAttribute("x_gap", "local_name", "s3gapX");
		beamDefAp.setAttribute("x_gap", "controller_record", "EPICS::s3gapX");
		beamDefAp.setY_gapScalar(1.5);
		beamDefAp.setAttribute("y_gap", "units", "mm");
		beamDefAp.setAttribute("y_gap", "local_name", "s3gapY");
		beamDefAp.setAttribute("y_gap", "controller_record", "EPICS::s3gapY");
		beamDefAp.addGroupNode("transforms", NexusNodeFactory.createNXtransformations());//TODO Basham
		
		NXbeam beamDefApBeam = NexusNodeFactory.createNXbeam();
		/**
		 * !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		 * TODO Not sure what's wrong here:
		 * - third line (i.e. the one I want) fails.
		 * !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		 */
		beamDefApBeam.addSymbolicNode("incident_wavelength_spread", NexusNodeFactory.createSymbolicNode(XPDFTestUtils.getNexusTree().getSourceURI(), "/entry1/instrument/bent_laue_monochromator/beam/final_wavelength_spread"));
//		beamDefApBeam.addSymbolicNode("incident_wavelength_spread", NexusNodeFactory.createSymbolicNode(nexusTree.getSourceURI(), "/entry1/instrument/secondary_slit/beam/final_wavelength_spread"));
//		beamDefApBeam.addSymbolicNode("incident_wavelength_spread", NexusNodeFactory.createSymbolicNode(nexusTree.getSourceURI(), "/entry1/instrument/multi_layer_mirror/beam/final_wavelength_spread"));
		beamDefApBeam.setFinal_wavelength_spreadScalar(0.0008);
		beamDefApBeam.addSymbolicNode("incident_beam_divergence", NexusNodeFactory.createSymbolicNode(XPDFTestUtils.getNexusTree().getSourceURI(), "/entry1/instrument/multi_layer_mirror/beam/final_beam_divergence"));
		beamDefApBeam.setFinal_beam_divergence(DatasetFactory.createFromObject(new double[]{0.20, 0.55}, new int[]{2})); //TODO Numbers will be needed from Phil
		beamDefApBeam.setAttribute("final_beam_divergence", "units", "radians");
		beamDefAp.addGroupNode("beam", beamDefApBeam);

		NXcollection beamDefApMotors = NexusNodeFactory.createNXcollection(); //TODO NXstage
		NXpositioner xCentre = NexusNodeFactory.createNXpositioner();
		xCentre.setNameScalar("s3cenX");
		xCentre.setDescriptionScalar("Slit X position");
		xCentre.setValueScalar(1.258);
		xCentre.setAttribute("value", "units", "mm");
		beamDefApMotors.addGroupNode("x_centre", xCentre);
		beamDefApMotors.setAttribute("x_centre", "controller_record", "EPICS::s3cenX");
		NXpositioner yCentre = NexusNodeFactory.createNXpositioner();
		yCentre.setNameScalar("s3cenY");
		yCentre.setDescriptionScalar("Inboard slit X motor");
		yCentre.setValueScalar(3.25);
		yCentre.setAttribute("value", "units", "mm");
		beamDefApMotors.addGroupNode("y_centre", yCentre);
		beamDefApMotors.setAttribute("y_centre", "controller_record", "EPICS::s3cenY");
		NXpositioner xGap = NexusNodeFactory.createNXpositioner();
		xGap.setNameScalar("s3gapX");
		xGap.setDescriptionScalar("Slit X gap");
		xGap.setValueScalar(1.7);
		xGap.setAttribute("value", "units", "mm");
		beamDefApMotors.addGroupNode("x_gap", xGap);
		beamDefApMotors.setAttribute("x_gap", "controller_record", "EPICS::s3gapX");
		NXpositioner yGap = NexusNodeFactory.createNXpositioner();
		yGap.setNameScalar("s3gapY");
		yGap.setDescriptionScalar("Slit Y gap");
		yGap.setValueScalar(1.5);
		yGap.setAttribute("value", "units", "mm");
		beamDefApMotors.addGroupNode("y_gap", yGap);
		beamDefApMotors.setAttribute("y_gap", "controller_record", "EPICS::s3gapY");
		beamDefAp.addGroupNode("motors", beamDefApMotors);
	}
	
	private static void populateFirstSampleSlit(NXinstrument instrument) {
		NXslit firstSampleSlit = instrument.getChild("first_sample_slit", NXslit.class);
		
		/*
		 * Beam defining slits
		 */
		firstSampleSlit.setX_gapScalar(1.7);
		firstSampleSlit.setAttribute("x_gap", "units", "mm");
		firstSampleSlit.setAttribute("x_gap", "local_name", "s4gapX");
		firstSampleSlit.setAttribute("x_gap", "controller_record", "EPICS::s4gapX");
		firstSampleSlit.setY_gapScalar(1.5);
		firstSampleSlit.setAttribute("y_gap", "units", "mm");
		firstSampleSlit.setAttribute("y_gap", "local_name", "s4gapY");
		firstSampleSlit.setAttribute("y_gap", "controller_record", "EPICS::s4gapY");
		firstSampleSlit.addGroupNode("transforms", NexusNodeFactory.createNXtransformations());//TODO Basham
		
		NXbeam firstSampleSlitBeam = NexusNodeFactory.createNXbeam();
		firstSampleSlitBeam.setIncident_beam_divergence(DatasetFactory.createFromObject(new double[]{0.4, 0.98}, new int[]{2})); //TODO Numbers will be needed from Phil
		firstSampleSlitBeam.setAttribute("incident_beam_divergence", "units", "radians");
		firstSampleSlitBeam.setFinal_beam_divergence(DatasetFactory.createFromObject(new double[]{0.3, 0.7}, new int[]{2})); //TODO Numbers will be needed from Phil
		firstSampleSlitBeam.setAttribute("final_beam_divergence", "units", "radians");
		firstSampleSlit.addGroupNode("beam", firstSampleSlitBeam);

		NXcollection firstSampleSlitMotors = NexusNodeFactory.createNXcollection(); //TODO NXstage
		NXpositioner xCentre = NexusNodeFactory.createNXpositioner();
		xCentre.setNameScalar("s4cenX");
		xCentre.setDescriptionScalar("Slit X position");
		xCentre.setValueScalar(1.258);
		xCentre.setAttribute("value", "units", "mm");
		firstSampleSlitMotors.addGroupNode("x_centre", xCentre);
		firstSampleSlitMotors.setAttribute("x_centre", "controller_record", "EPICS::s4cenX");
		NXpositioner yCentre = NexusNodeFactory.createNXpositioner();
		yCentre.setNameScalar("s4cenY");
		yCentre.setDescriptionScalar("Inboard slit X motor");
		yCentre.setValueScalar(3.25);
		yCentre.setAttribute("value", "units", "mm");
		firstSampleSlitMotors.addGroupNode("y_centre", yCentre);
		firstSampleSlitMotors.setAttribute("y_centre", "controller_record", "EPICS::s4cenY");
		NXpositioner xGap = NexusNodeFactory.createNXpositioner();
		xGap.setNameScalar("s4gapX");
		xGap.setDescriptionScalar("Slit X gap");
		xGap.setValueScalar(1.7);
		xGap.setAttribute("value", "units", "mm");
		firstSampleSlitMotors.addGroupNode("x_gap", xGap);
		firstSampleSlitMotors.setAttribute("x_gap", "controller_record", "EPICS::s4gapX");
		NXpositioner yGap = NexusNodeFactory.createNXpositioner();
		yGap.setNameScalar("s4gapY");
		yGap.setDescriptionScalar("Slit Y gap");
		yGap.setValueScalar(1.5);
		yGap.setAttribute("value", "units", "mm");
		firstSampleSlitMotors.addGroupNode("y_gap", yGap);
		firstSampleSlitMotors.setAttribute("y_gap", "controller_record", "EPICS::s4gapY");
		firstSampleSlit.addGroupNode("motors", firstSampleSlitMotors);
	}
	
	private static void populateSecondSampleSlit(NXinstrument instrument) {
		NXslit secondSampleSlit = instrument.getChild("second_sample_slit", NXslit.class);
		
		/*
		 * Beam defining slits
		 */
		secondSampleSlit.setX_gapScalar(1.7);
		secondSampleSlit.setAttribute("x_gap", "units", "mm");
		secondSampleSlit.setAttribute("x_gap", "local_name", "s5gapX");
		secondSampleSlit.setAttribute("x_gap", "controller_record", "EPICS::s5gapX");
		secondSampleSlit.setY_gapScalar(1.5);
		secondSampleSlit.setAttribute("y_gap", "units", "mm");
		secondSampleSlit.setAttribute("y_gap", "local_name", "s5gapY");
		secondSampleSlit.setAttribute("y_gap", "controller_record", "EPICS::s5gapY");
		secondSampleSlit.addGroupNode("transforms", NexusNodeFactory.createNXtransformations());//TODO Basham
		
		NXbeam secondSampleSlitBeam = NexusNodeFactory.createNXbeam();
		secondSampleSlitBeam.setIncident_beam_divergence(DatasetFactory.createFromObject(new double[]{0.4, 0.98}, new int[]{2})); //TODO Numbers will be needed from Phil
		secondSampleSlitBeam.setAttribute("incident_beam_divergence", "units", "radians");
		secondSampleSlitBeam.setFinal_beam_divergence(DatasetFactory.createFromObject(new double[]{0.3, 0.7}, new int[]{2})); //TODO Numbers will be needed from Phil
		secondSampleSlitBeam.setAttribute("final_beam_divergence", "units", "radians");
		secondSampleSlit.addGroupNode("beam", secondSampleSlitBeam);

		NXcollection secondSampleSlitMotors = NexusNodeFactory.createNXcollection(); //TODO NXstage
		NXpositioner xCentre = NexusNodeFactory.createNXpositioner();
		xCentre.setNameScalar("s5cenX");
		xCentre.setDescriptionScalar("Slit X position");
		xCentre.setValueScalar(1.258);
		xCentre.setAttribute("value", "units", "mm");
		secondSampleSlitMotors.addGroupNode("x_centre", xCentre);
		secondSampleSlitMotors.setAttribute("x_centre", "controller_record", "EPICS::s5cenX");
		NXpositioner yCentre = NexusNodeFactory.createNXpositioner();
		yCentre.setNameScalar("s5cenY");
		yCentre.setDescriptionScalar("Inboard slit X motor");
		yCentre.setValueScalar(3.25);
		yCentre.setAttribute("value", "units", "mm");
		secondSampleSlitMotors.addGroupNode("y_centre", yCentre);
		secondSampleSlitMotors.setAttribute("y_centre", "controller_record", "EPICS::s5cenY");
		NXpositioner xGap = NexusNodeFactory.createNXpositioner();
		xGap.setNameScalar("s5gapX");
		xGap.setDescriptionScalar("Slit X gap");
		xGap.setValueScalar(1.7);
		xGap.setAttribute("value", "units", "mm");
		secondSampleSlitMotors.addGroupNode("x_gap", xGap);
		secondSampleSlitMotors.setAttribute("x_gap", "controller_record", "EPICS::s5gapX");
		NXpositioner yGap = NexusNodeFactory.createNXpositioner();
		yGap.setNameScalar("s5gapY");
		yGap.setDescriptionScalar("Slit Y gap");
		yGap.setValueScalar(1.5);
		yGap.setAttribute("value", "units", "mm");
		secondSampleSlitMotors.addGroupNode("y_gap", yGap);
		secondSampleSlitMotors.setAttribute("y_gap", "controller_record", "EPICS::s5gapY");
		secondSampleSlit.addGroupNode("motors", secondSampleSlitMotors);
	}
	
	private static void populateI0Monitor(NXinstrument instrument, long durationSecs) {
		NXmonitor bpm3 = instrument.getChild("i0_beam_position_monitor_3", NXmonitor.class);
		bpm3.setAttribute(null, "local_name", "bpm3");
		bpm3.setField("description", "Diamond quadrant I0 monitor");
		bpm3.setTypeScalar("Diamond quadrant beam position monitor");
		//TODO Do we want any data here? e.g. data, count_time, x/y_centre, x/y_size 
		bpm3.setField("status", "in");
		bpm3.setData(DatasetFactory.createLinearSpace(DoubleDataset.class, 8, 8, (int)durationSecs));
		bpm3.setCount_timeScalar(new Double(durationSecs));
		bpm3.setField("x_centre", 1.2);
		bpm3.setAttribute("x_centre", "units", "mm");
		bpm3.setField("y_centre", 0.8);
		bpm3.setAttribute("y_centre", "units", "mm");
		bpm3.setDistanceScalar(-0.2); //This is made up
		bpm3.setAttribute("distance", "units", "m");

		NXcollection quadrants = NexusNodeFactory.createNXcollection();
		NXmonitor quad1 = NexusNodeFactory.createNXmonitor();
		quad1.setAttribute(null, "local_name", "bpm3q1");
		quad1.setAttribute(null, "controller_record", "EPICS::bpm3q1");
		quad1.setData(DatasetFactory.createLinearSpace(DoubleDataset.class, 2, 2, (int)durationSecs));
		quad1.setAttribute("data", "units", "counts");
		quadrants.addGroupNode("quadrant_1", quad1);
		NXmonitor quad2 = NexusNodeFactory.createNXmonitor();
		quad2.setAttribute(null, "local_name", "bpm3q1");
		quad2.setAttribute(null, "controller_record", "EPICS::bpm3q1");
		quad2.setData(DatasetFactory.createLinearSpace(DoubleDataset.class, 2, 2, (int)durationSecs));
		quad2.setAttribute("data", "units", "counts");
		quadrants.addGroupNode("quadrant_2", quad2);
		NXmonitor quad3 = NexusNodeFactory.createNXmonitor();
		quad3.setAttribute(null, "local_name", "bpm3q1");
		quad3.setAttribute(null, "controller_record", "EPICS::bpm3q1");
		quad3.setData(DatasetFactory.createLinearSpace(DoubleDataset.class, 2, 2, (int)durationSecs));
		quad3.setAttribute("data", "units", "counts");
		quadrants.addGroupNode("quadrant_3", quad3);
		NXmonitor quad4 = NexusNodeFactory.createNXmonitor();
		quad4.setAttribute(null, "local_name", "bpm3q1");
		quad4.setAttribute(null, "controller_record", "EPICS::bpm3q1");
		quad4.setData(DatasetFactory.createLinearSpace(DoubleDataset.class, 2, 2, (int)durationSecs));
		quad4.setAttribute("data", "units", "counts");
		quadrants.addGroupNode("quadrant_4", quad4);
	}

	private static void populateDetector1(NXinstrument instrument, long durationSecs) {
		NXdetector det1 = instrument.getChild("detector_1", NXdetector.class);
		populateDet(det1, durationSecs);
	}
	
	private static void populateDetector2(NXinstrument instrument, long durationSecs) {
		NXdetector det2 = instrument.getChild("detector_2", NXdetector.class);
		populateDet(det2, durationSecs);
	}
		
	private static void populateDet(NXdetector det1, long durationSecs) {
		
		//Detector information
		det1.setLocal_nameScalar("det1");
		det1.setDescriptionScalar("Perkin Elmer XRD1611 CP3");
		det1.setTypeScalar("CsI scintillator/a-Si TFT pixel detector");
		det1.setLayoutScalar("area");
		//pixel info
		det1.setX_pixel_sizeScalar(0.2);
		det1.setAttribute("x_pixel_size", "units", "mm");
		det1.setY_pixel_sizeScalar(0.2);
		det1.setAttribute("y_pixel_size", "units", "mm");
		//mode
		det1.setGain_settingScalar("0.25");
		det1.setAttribute("gain_setting", "units", "pF");
		det1.setGain_settingScalar("1.0");
		det1.setAttribute("gain_setting", "units", "pF");
		det1.setField("sensor_density", 4.28);
		det1.setAttribute("sensor_density", "units", "g cm-3");
		
		//Data collection
		//timings
		det1.setCount_timeScalar(durationSecs);
		det1.setAttribute("count_time", "units", "s");
		det1.setFrame_timeScalar(1.);
		det1.setAttribute("frame_time", "units", "s");
		//processing
//		try{
////			d1.setPixel_mask_appliedScalar(false); //TODO DAQ-614
//			String maskPath = null;//"/dls/science/groups/das/ExampleData/i15-1/integration/128991_mask_min1000_max30000.nxs";
//			Dataset pxMask = DatasetUtils.sliceAndConvertLazyDataset(ProcessingUtils.getLazyDataset(null, maskPath, "/entry/mask/128911 min 1000 max 30000 plus additional pixels"));
//			det1.setPixel_mask(pxMask);
//			
////			d1.setFlatfield_appliedScalar(true); //TODO DAQ-614
			String flatPath = null; 
//			Dataset flatField = DatasetUtils.sliceAndConvertLazyDataset(ProcessingUtils.getLazyDataset(null, flatPath, "/entry/mask/128911 min 1000 max 30000 plus additional pixels"));
//			det1.setFlatfield(flatField);
//		} catch (DatasetException de) {
//			System.err.println("Failed to set external data proc dataset");
//		}
		

		// Calibration method copied exactly from output calibration nexus file
		// Transformation, by hand from the calibration file
		det1.setBeam_center_xScalar(1057.3957);
		det1.setBeam_center_yScalar(1028.0555);
		NXnote calNote = NexusNodeFactory.createNXnote();
		calNote.setAuthorScalar("DAWNScience");
		calNote.setDataset("d_space_index", DatasetFactory.createFromObject(new double[]{1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 13.0, 18.0, 19.0}));
		calNote.setDescriptionScalar("Manual powder diffraction image calibration using point parameters");
		calNote.setDataset("residual", DatasetFactory.createFromObject(new double[] {4527590406716483326.0}));
		det1.addGroupNode("calibration_method", calNote);
		
		// calibration data - TODO shouldn't data be real data rather than calibration?
		String calPath = null;//"/dls/science/groups/das/ExampleData/i15-1/integration/CeO2_NIST_8s_19slices_averaged_fixedE_calibration.nxs";
//		try {
//			Dataset calData = DatasetUtils.sliceAndConvertLazyDataset(ProcessingUtils.getLazyDataset(null, calPath, "/entry/instrument/detector/data"));
//			det1.setData(calData);
//		} catch (DatasetException dE) {
//			System.err.println("Failed to set external calibration dataset");
//		}
		// detector orientation matrix
		det1.setDataset("detector_orientation", DatasetFactory.createFromObject(new double[]{
				-0.28420125, 0.95876440, -0.00069477874,
				-0.95876153, -0.28420210, -0.0023438571,
				-0.0024446643, 0.0000000, 0.99999701}));
		// distance
		det1.setDistanceScalar(237.29744);
		det1.setAttribute("distance", "units", "mm");
		// pixel size and number
		// pixel size already set in the specified detector values
		det1.setDataset("x_pixel_number", DatasetFactory.createFromObject( new double[]{2048}));
		det1.setDataset("y_pixel_number", DatasetFactory.createFromObject( new double[]{2048}));
	}
}
