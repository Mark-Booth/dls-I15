package uk.ac.diamond.xpdf.test;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.Date;

import org.eclipse.dawnsci.hdf5.nexus.NexusFileFactoryHDF5;
import org.eclipse.dawnsci.nexus.NXentry;
import org.eclipse.dawnsci.nexus.NXinstrument;
import org.eclipse.dawnsci.nexus.NXroot;
import org.eclipse.dawnsci.nexus.NXuser;
import org.eclipse.dawnsci.nexus.NexusException;
import org.eclipse.dawnsci.nexus.NexusNodeFactory;
import org.eclipse.dawnsci.nexus.ServiceHolder;
import org.eclipse.dawnsci.nexus.builder.NexusFileBuilder;
import org.eclipse.dawnsci.nexus.builder.impl.DefaultNexusFileBuilder;
import org.junit.After;
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
	
	@After
	public void tearDown() {
		XPDFInstrumentNexusSpec.setNexusTree(null);
	}
	
	@Test
	public void testEmptyBeamlineNeXusWriting() throws NexusException {
		nexusBuilder = new DefaultNexusFileBuilder(testScratchDirectoryName+beamlineFileName);
		XPDFInstrumentNexusSpec.setNexusTree(nexusBuilder.getNexusTree());
		NXroot root = nexusBuilder.getNXroot();
		root.setAttributeFile_name(testScratchDirectoryName+beamlineFileName);

		long experimentDuration = 600;
		createBasicStructure(root, experimentDuration);
		
		//These are the last two fields to populate
		Date endTime = Date.from(fakeNow.plusSeconds(experimentDuration));
		NXentry entry = root.getChild("entry1", NXentry.class);
		entry.setEnd_timeScalar(endTime);
		root.setAttributeFile_time(endTime.toString());

		nexusBuilder.createFile(false).close();
		System.out.println("Success writing NeXus file to " + testScratchDirectoryName+beamlineFileName);
	}
	
	@Test
	public void testContainerNeXusWriting() throws NexusException {
		nexusBuilder = new DefaultNexusFileBuilder(testScratchDirectoryName+containerFileName);
		XPDFInstrumentNexusSpec.setNexusTree(nexusBuilder.getNexusTree());
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

		nexusBuilder.createFile(false).close();
		System.out.println("Success writing NeXus file to " + testScratchDirectoryName+containerFileName);
	}
	
	@Test
	public void testSampleNeXusWriting() throws NexusException {
		nexusBuilder = new DefaultNexusFileBuilder(testScratchDirectoryName+sampleFilename);
		XPDFInstrumentNexusSpec.setNexusTree(nexusBuilder.getNexusTree());
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

		nexusBuilder.createFile(false).close();
		System.out.println("Success writing NeXus file to " + testScratchDirectoryName+sampleFilename);
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
		
		XPDFInstrumentNexusSpec.populateNXinstrument(entry.getChild("instrument", NXinstrument.class), fakeNow, durationSecs);
		populateNXusers(entry);
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
