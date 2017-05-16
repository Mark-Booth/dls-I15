package uk.ac.diamond.xpdf.test;

import java.io.File;
import java.util.Date;

import org.eclipse.dawnsci.hdf5.nexus.NexusFileFactoryHDF5;
import org.eclipse.dawnsci.nexus.INexusFileFactory;
import org.eclipse.dawnsci.nexus.NXentry;
import org.eclipse.dawnsci.nexus.NXroot;
import org.eclipse.dawnsci.nexus.NexusException;
import org.eclipse.dawnsci.nexus.NexusFile;
import org.eclipse.dawnsci.nexus.ServiceHolder;
import org.eclipse.dawnsci.nexus.builder.NexusFileBuilder;
import org.eclipse.dawnsci.nexus.builder.impl.DefaultNexusFileBuilder;
import org.eclipse.january.dataset.DatasetFactory;
import org.eclipse.january.dataset.IDataset;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

import hdf.hdf5lib.H5;
import uk.ac.diamond.scisoft.analysis.io.LoaderServiceImpl;
import uk.ac.diamond.scisoft.analysis.processing.LocalServiceManager;

public class XPDFNexusWritingTest {
	
	private static String testScratchDirectoryName;
	private static final String beamlineFileName = "empty-xpdf.nxs",
								containerFileName = "capillary-xpdf.nxs",
								sampleFilename = "capillary_sample-xpdf.nxs";
//	private static String FILE_NAME; TODO Delete
//	private static String FILE2_NAME;
	private NexusFileBuilder nexusBuilder;
	
	@BeforeClass
	public static void setUpBeforeClass() throws Exception {
		testScratchDirectoryName = TestUtils.generateDirectorynameFromClassname(XPDFNexusWritingTest.class.getName());
		TestUtils.makeScratchDirectory(testScratchDirectoryName);
//		(new File(testScratchDirectoryName + "origin/")).mkdirs(); TODO Delete
//		(new File(testScratchDirectoryName + "linked/")).mkdirs();
//		FILE_NAME = testScratchDirectoryName + "test.nxs";
//		FILE2_NAME = testScratchDirectoryName + "ext-test.nxs";
		System.setProperty("java.library.path",System.getProperty("java.library.path")+";C:\\ecl-ws\\scanning-ws_min\\dawn-hdf.git\\hdf.hdf5lib;C:\\ecl-ws\\scanning-ws_min\\dawn-hdf.git\\hdf.hdf5lib\\lib\\win32-x86_64");
		
		
	}
	
	@Before
	public void setup() {
		//Set services which will handle the file creation/reading
		ServiceHolder.setNexusFileFactory(new NexusFileFactoryHDF5());
//		LocalServiceManager.setLoaderService(new LoaderServiceImpl()); TODO Needed?
		
		
	}
	
	@Test
	public void testEmptyBeamlineNexusWriting() {
		System.out.println(System.getProperty("java.library.path"));
		
		nexusBuilder = new DefaultNexusFileBuilder(testScratchDirectoryName+beamlineFileName);
		NXroot root = nexusBuilder.getNXroot();
		
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
		root.setAttributeFile_name(testScratchDirectoryName+beamlineFileName);
		root.setAttributeFile_time(new Date().toString());
		
		NXentry entry = root.getChild("entry1", NXentry.class);
//		entry.setStart_time(null);
		
//		IDataset start = DatasetFactory.
		
		
		try {
			nexusBuilder.createFile(false).close();
			System.err.println("Success writing NeXus file to " + testScratchDirectoryName+beamlineFileName);
		} catch (NexusException nE) {
			System.err.println("Error writing NeXus file to " + testScratchDirectoryName+beamlineFileName + ": " + nE.toString());
		}
		
		}
		/*
		 * @file_time = now
		 * @file_name = real path
		 * /entry/start_time = 12.05.2017 17:31
		 * /entry/end_time = 12.05.2017 18:45
		 * /entry/duration = 74*60 seconds
		 * /entry/entry_identifier = 2795
		 * /entry/experiment_identifier = ee15900
		 * /entry/program_name = GDA @version = 9.4pre
		 */
		

}
