package uk.ac.diamond.xpdf.test;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.Date;

import org.eclipse.dawnsci.analysis.api.tree.DataNode;
import org.eclipse.dawnsci.hdf5.nexus.NexusFileFactoryHDF5;
import org.eclipse.dawnsci.nexus.NXentry;
import org.eclipse.dawnsci.nexus.NXinstrument;
import org.eclipse.dawnsci.nexus.NXroot;
import org.eclipse.dawnsci.nexus.NXsource;
import org.eclipse.dawnsci.nexus.NXuser;
import org.eclipse.dawnsci.nexus.NexusException;
import org.eclipse.dawnsci.nexus.NexusNodeFactory;
import org.eclipse.dawnsci.nexus.ServiceHolder;
import org.eclipse.dawnsci.nexus.builder.NexusFileBuilder;
import org.eclipse.dawnsci.nexus.builder.impl.DefaultNexusFileBuilder;
import org.eclipse.january.dataset.DatasetFactory;
import org.eclipse.january.dataset.DoubleDataset;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

public class XPDFNexusWritingTest {
	
	private static String testScratchDirectoryName;
	private static final String beamlineFileName = "empty-xpdf.nxs",
								containerFileName = "capillary-xpdf.nxs",
								sampleFilename = "capillary_sample-xpdf.nxs";
	private NexusFileBuilder nexusBuilder;
	
	private Instant fakeNow;
	
	@BeforeClass
	public static void setUpBeforeClass() throws Exception {
		testScratchDirectoryName = TestUtils.generateDirectorynameFromClassname(XPDFNexusWritingTest.class.getSimpleName());
		TestUtils.makeScratchDirectory(testScratchDirectoryName); 
	}
	
	@Before
	public void setup() {
		//Set services which will handle the file creation/reading
		ServiceHolder.setNexusFileFactory(new NexusFileFactoryHDF5());
//		LocalServiceManager.setLoaderService(new LoaderServiceImpl()); TODO Needed?
		
		fakeNow = LocalDateTime.of(2017, 5, 16, 12, 24, 6).atZone(ZoneId.of("Europe/London")).toInstant();
	}
	
	@Test
	public void testEmptyBeamlineNeXusWriting() {
		nexusBuilder = new DefaultNexusFileBuilder(testScratchDirectoryName+beamlineFileName);
		NXroot root = nexusBuilder.getNXroot();
		root.setAttributeFile_name(testScratchDirectoryName+beamlineFileName);

		long experimentDuration = 600;
		createBasicStructure(root, experimentDuration);
		
		//These are the last two fields to populate
		Date endTime = Date.from(fakeNow.plusSeconds(experimentDuration));
		NXentry entry = root.getChild("entry1", NXentry.class);
		entry.setEnd_timeScalar(endTime);
		root.setAttributeFile_time(endTime.toString());

		try {
			nexusBuilder.createFile(false).close();
			System.out.println("Success writing NeXus file to " + testScratchDirectoryName+beamlineFileName);
		} catch (NexusException nE) {
			System.err.println("Error writing NeXus file to " + testScratchDirectoryName+beamlineFileName + ": " + nE.toString());
		}

	}
	
	@Test
	public void testContainerNeXusWriting() {
		nexusBuilder = new DefaultNexusFileBuilder(testScratchDirectoryName+containerFileName);
		NXroot root = nexusBuilder.getNXroot();
		root.setAttributeFile_name(testScratchDirectoryName+containerFileName);
		
		long experimentDuration = 600;
		createBasicStructure(root, experimentDuration);
		
		NXentry entry = root.getChild("entry1", NXentry.class);
		entry.addGroupNode("sample", NexusNodeFactory.createNXsample());
		
		//These are the last two fields to populate
		Date endTime = Date.from(fakeNow.plusSeconds(experimentDuration));
		entry.setEnd_timeScalar(endTime);
		root.setAttributeFile_time(endTime.toString());

		try {
			nexusBuilder.createFile(false).close();
			System.out.println("Success writing NeXus file to " + testScratchDirectoryName+containerFileName);
		} catch (NexusException nE) {
			System.err.println("Error writing NeXus file to " + testScratchDirectoryName+containerFileName + ": " + nE.toString());
		}
	}
	
	@Test
	public void testSampleNeXusWriting() {
		nexusBuilder = new DefaultNexusFileBuilder(testScratchDirectoryName+sampleFilename);
		NXroot root = nexusBuilder.getNXroot();
		root.setAttributeFile_name(testScratchDirectoryName+sampleFilename);

		long experimentDuration = 600;
		createBasicStructure(root, experimentDuration);
		
		NXentry entry = root.getChild("entry1", NXentry.class);
		entry.addGroupNode("sample", NexusNodeFactory.createNXsample());
		
		//These are the last two fields to populate
		Date endTime = Date.from(fakeNow.plusSeconds(experimentDuration));
		entry.setEnd_timeScalar(endTime);
		root.setAttributeFile_time(endTime.toString());

		try {
			nexusBuilder.createFile(false).close();
			System.out.println("Success writing NeXus file to " + testScratchDirectoryName+sampleFilename);
		} catch (NexusException nE) {
			System.err.println("Error writing NeXus file to " + testScratchDirectoryName+sampleFilename + ": " + nE.toString());
		}
	}
	
	private void createBasicStructure(NXroot root, long durationSecs) {
		/*
		 * @file_time = now
		 * @file_name = real path
		 * /entry/start_time = 12.05.2017 17:10
		 * /entry/end_time = 12.05.2017 17:20
		 * /entry/duration = 600 seconds
		 * /entry/entry_identifier = 2793
		 * /entry/experiment_identifier = ee15900
		 * /entry/program_name = GDA @version = 9.4pre
		 */
		root.addGroupNode("entry1", NexusNodeFactory.createNXentry());
		NXentry entry = root.getChild("entry1", NXentry.class);
		entry.setStart_timeScalar(Date.from(fakeNow));
		entry.setExperiment_identifierScalar("ee15900");
		entry.setEntry_identifierScalar("2793");
		entry.setProgram_nameScalar("GDA");
		entry.setProgram_nameAttributeVersion("9.4pre");
		entry.setDurationScalar(durationSecs);
		entry.setAttribute("duration", "units", "s");
		
		/*
		 * Other nodes
		 * instrument:NXinstrument
		 * sample:NXsample
		 * data:NXdata
		 * principal_investigator:NXuser
		 * user:NXuser (currently logged in)
		 * local_contact:NXuser
		 */
		entry.addGroupNode("instrument", NexusNodeFactory.createNXinstrument());
		entry.addGroupNode("data", NexusNodeFactory.createNXdata());
		entry.addGroupNode("principal_investigator", NexusNodeFactory.createNXuser());
		entry.addGroupNode("user", NexusNodeFactory.createNXuser());
		entry.addGroupNode("local_contact", NexusNodeFactory.createNXuser());
		
		populateNXinstrument(entry.getChild("instrument", NXinstrument.class), durationSecs);
		populateNXusers(entry);
	}
	
	private void populateNXinstrument(NXinstrument instrument, long durationSecs) {
		//Set names
		instrument.setNameScalar("i15-1");
		DataNode dn = NexusNodeFactory.createDataNode();
		dn.setDataset(DatasetFactory.createFromObject(new String[]{"XPDF"}, new int[]{1}));
		instrument.addDataNode("alt_name", dn);
		
		//Add beamline devices
		instrument.addGroupNode("insertion_device", NexusNodeFactory.createNXinsertion_device());
		instrument.addGroupNode("primary_slit", NexusNodeFactory.createNXslit());
		instrument.addGroupNode("attenuator_1", NexusNodeFactory.createNXattenuator());
		instrument.addGroupNode("attenuator_2", NexusNodeFactory.createNXattenuator());
		instrument.addGroupNode("attenuator_3", NexusNodeFactory.createNXattenuator());
		instrument.addGroupNode("bent_laue_monochromator", NexusNodeFactory.createNXmonochromator());
		instrument.addGroupNode("beam_position_monitor_1", NexusNodeFactory.createNXmonitor());
		instrument.addGroupNode("secondary_slit", NexusNodeFactory.createNXslit());
		instrument.addGroupNode("multilayer_mirror", NexusNodeFactory.createNXmirror());
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
		
		//Source
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
		source.setLast_fillAttributeTime(Date.from(fakeNow.minusSeconds(487)));
//		source. notes
		source.setDistanceScalar(-35.5);
		source.setAttribute("distance", "units", "m");
		instrument.setSource(source);
	}
	
	private void populateNXusers(NXentry entry) {
		//PI - i.e. the one on the beach
		NXuser pi = entry.getChild("principal_investigator", NXuser.class);
		pi.setNameScalar("Isaac Porthau");
		pi.setRoleScalar("Principal investigator");
		pi.setFacility_user_idScalar("msk14411");
		pi.setAffiliationScalar("Musketeers of the Guard");
		
		//User - i.e. the one that is collecting the data
		NXuser user = entry.getChild("user", NXuser.class);
		user.setNameScalar("Armand Athos");
		user.setRoleScalar("User responsible for data collection");
		user.setFacility_user_idScalar("msk41141");
		pi.setAffiliationScalar("Musketeers of the Guard");
		
		//Local contact
		NXuser contact = entry.getChild("local_contact", NXuser.class);
		contact.setNameScalar("Henri Aramitz");
		contact.setRoleScalar("Local contact");
		contact.setFacility_user_idScalar("msk00003");
		contact.setEmailScalar("nota.realaddr@diamond.ac.uk");
		contact.setTelephone_numberScalar("+44 1235 77 9999");
	}


}
