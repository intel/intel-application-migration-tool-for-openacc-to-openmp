
























<!DOCTYPE html>

<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" /><meta name="generator" content="Docutils 0.17.1: http://docutils.sourceforge.net/" />

    <title>Security Vulnerability Handling &#8212; OpenEcosystem Portal</title>
    
  <link href="../_static/css/theme.css" rel="stylesheet">
  <link href="../_static/css/index.ff1ffe594081f20da1ef19478df9384b.css" rel="stylesheet">

    
  <link rel="stylesheet"
    href="../_static/vendor/fontawesome/5.13.0/css/all.min.css">
  <link rel="preload" as="font" type="font/woff2" crossorigin
    href="../_static/vendor/fontawesome/5.13.0/webfonts/fa-solid-900.woff2">
  <link rel="preload" as="font" type="font/woff2" crossorigin
    href="../_static/vendor/fontawesome/5.13.0/webfonts/fa-brands-400.woff2">

    
      

    
    <link rel="stylesheet" type="text/css" href="../_static/pygments.css" />
    <link rel="stylesheet" type="text/css" href="../_static/css/blank.css" />
    <link rel="stylesheet" type="text/css" href="../_static/bootstrap-icons/font/bootstrap-icons.css" />
    <link rel="stylesheet" type="text/css" href="../_static/dlux-bootstrap/css/dlux.min.css" />
    <link rel="stylesheet" type="text/css" href="../_static/OSPO/css/ospo.css" />
    <link rel="stylesheet" type="text/css" href="../_static/star-rating.js/dist/star-rating.css" />
    
  <link rel="preload" as="script" href="../_static/js/index.be7d3bbb2ef33a8344ce.js">

    <script data-url_root="../" id="documentation_options" src="../_static/documentation_options.js"></script>
    <script src="../_static/jquery.js"></script>
    <script src="../_static/underscore.js"></script>
    <script src="../_static/doctools.js"></script>
    <script src="../_static/rss-parser/rss-parser.min.js"></script>
    <script src="../_static/OSPO/js/ospo.js"></script>
    <script src="../_static/OSPO/js/slider.js"></script>
    <script src="../_static/star-rating.js/dist/star-rating.js"></script>
    <script src="../_static/dayjs/dayjs.min.js"></script>
    <link rel="index" title="Index" href="../genindex.html" />
    <link rel="search" title="Search" href="../search.html" />
    <link rel="next" title="CVE Management of 3rd Party Components" href="Cvesecuritymanagement.html" />
    <link rel="prev" title="Review System" href="Reviewsystem.html" />
    
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="docsearch:language" content="None">
    

    <!-- Google Analytics -->
    
    
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-2N6KKNN0T3"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-2N6KKNN0T3');
    </script>


  </head>

  <body class="m-0 p-0" data-spy="scroll" data-target="#bd-toc-nav" offset="100">

	

		
		<div class="navbar-row sticky-top">
            





 


<nav class="top-navbar navbar navbar-expand-xl navbar-light px-1" >
  <a class="navbar-brand" href="
    
        
            
            ../index.html 
        
    ">            
        
        
        
            <span class="text-dark" style="font-size: 28px"><b>open</b>source.intel.com</span>
        
  </a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent">
    <i class="intelicon-menu"></i>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav justify-content-center mx-auto flex-wrap">
      
      
        
         
        

    
    
        <div class="nav-item dropdown align-items-center d-flex">
            <button class="btn dropdown-toggle nav-item border-0 text-uppercase text-dark" type="button"
                data-bs-toggle="dropdown" data-toggle="dropdown">
                Learning
            </button>
            <ul class="dropdown-menu dropdown-menu-left border-0">
                
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Learning.html 
        
    ">Learning</a>
            
            
                <ul class="m-0">
                    
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/licensing/Licensingtraining.html 
        
    ">Licensing Training Classes</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Preparingtheproject.html 
        
    ">Preparing for an Open Source Project</a>
            
            
                <ul class="m-0">
                    
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Whatisopensource.html 
        
    ">What is Open Source Software?</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/community/code-of-conduct.html 
        
    ">Contributor Covenant Code of Conduct</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/licensing/Licensingtraining.html 
        
    ">Licensing Training Classes</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Settinguptheteam.html 
        
    ">Setting Up the Team</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Developingintheopen.html 
        
    ">Developing in the Open</a>
            
            
        
    

                </ul>
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Prelaunch.html 
        
    ">Pre-Launch Activities - Chronological</a>
            
            
                <ul class="m-0">
                    
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Strategicplanning.html 
        
    ">Strategic Planning</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Creatingopengovernance.html 
        
    ">Creating an Openly Governed Project Governance Model</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/licensing/Licensing.html 
        
    ">Licensing Basics and Training</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Opensourcelicensingreview.html 
        
    ">Open Source Software Licensing Review</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/projectmanagement/Projectmanagement.html 
        
    ">Project Management</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Advocacymarketing.html 
        
    ">Advocacy and Marketing</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Documentation.html 
        
    ">Documentation: Tips and Best Practices</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Webpresence.html 
        
    ">Web Presence</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Preparingaproject.html 
        
    ">Open Source Software Release Approval</a>
            
            
        
    

                </ul>
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Launch.html 
        
    ">Launching a Project</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Developmentandmaintenance.html 
        
    ">Development and Maintenance - Alphabetic</a>
            
            
                <ul class="m-0">
                    
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Cicd.html 
        
    ">CI/CD Continuous Integration and Deployment</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Documentation.html 
        
    ">Documentation: Tips and Best Practices</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Issuemanagement.html 
        
    ">Issue Management</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Releasestrategy.html 
        
    ">Release Strategy</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Reviewsystem.html 
        
    ">Review System</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            #
        
    ">Security Vulnerability Handling</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Cvesecuritymanagement.html 
        
    ">CVE Management of 3rd Party Components</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Supplychainsecurity.html 
        
    ">Supply Chain Security</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Testingstrategy.html 
        
    ">Testing Strategy</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Webpresence.html 
        
    ">Web Presence</a>
            
            
        
    

                </ul>
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Community.html 
        
    ">Working with the Community</a>
            
            
                <ul class="m-0">
                    
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Communicationchannels.html 
        
    ">Communication Channels</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Developeroutreach.html 
        
    ">Developer Outreach</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Developermeetups.html 
        
    ">Developer Meetups</a>
            
            
        
    

                </ul>
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../Learning/Exitingaproject.html 
        
    ">Exiting an Open Source Project</a>
            
            
        
    

                </ul>
            
        
    

            </ul>
        </div>
    

      
        
         
        

    
    
        <div class="nav-item dropdown align-items-center d-flex">
            <button class="btn dropdown-toggle nav-item border-0 text-uppercase text-dark" type="button"
                data-bs-toggle="dropdown" data-toggle="dropdown">
                The Open Source Approval Process
            </button>
            <ul class="dropdown-menu dropdown-menu-left border-0">
                
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../OverallApproval/OverallApproval.html 
        
    ">The Open Source Approval Process</a>
            
            
                <ul class="m-0">
                    
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../OverallApproval/security/security.html 
        
    ">Mandatory: Security Development Lifecycle</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../OverallApproval/os-pdt/OpenSourcePDT.html 
        
    ">Mandatory: Open Source PDT</a>
            
            
                <ul class="m-0">
                    
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../OverallApproval/os-pdt/approval-process.html 
        
    ">The OSPDT Approval Process</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../OverallApproval/os-pdt/pdt-approval-workflow.html 
        
    ">Open Source PDT Approval Workflow</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../OverallApproval/os-pdt/faq.html 
        
    ">OSPDT Frequently Asked Questions</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../OverallApproval/os-pdt/proj-repo-naming.html 
        
    ">Open Source Software and Repo Naming Guidelines</a>
            
            
        
    

                </ul>
            
        
    

                </ul>
            
        
    

            </ul>
        </div>
    

      
        
         
        

    
    
        <div class="nav-item dropdown align-items-center d-flex">
            <button class="btn dropdown-toggle nav-item border-0 text-uppercase text-dark" type="button"
                data-bs-toggle="dropdown" data-toggle="dropdown">
                External Collaboration Tools
            </button>
            <ul class="dropdown-menu dropdown-menu-right border-0">
                
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../ExtCollab.html 
        
    ">External Collaboration Tools</a>
            
            
                <ul class="m-0">
                    
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../ExtCollab/linux.intel.com.html 
        
    ">linux.intel.com email Accounts for Patches</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../ExtCollab/linux-ftp.html 
        
    ">linux-ftp Mirror Network</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../ExtCollab/sles-license-server.html 
        
    ">SLES License & Repo Server</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../ExtCollab/otcirc.html 
        
    ">OTCIRC Chat Services</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../ExtCollab/github-external.html 
        
    ">Github External Hosting</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../ExtCollab/jira.html 
        
    ">Jira Consulting & Hosting</a>
            
            
                <ul class="m-0">
                    
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../ExtCollab/opensourcejira.html 
        
    ">Open Source Instance Hosting</a>
            
            
        
    

                </ul>
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../ExtCollab/ssh-key-policy.html 
        
    ">SSH Keying Policy</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../ExtCollab/download.01.org.html 
        
    ">download.01.org CDN Services</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../ExtCollab/mailinglists.html 
        
    ">Mailing Lists</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../ExtCollab/readthedocs-hosting.html 
        
    ">Read the Docs Hosting Services</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../sphinx-bkms.html 
        
    ">Sphinx BKMs</a>
            
            
                <ul class="m-0">
                    
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../sphinx-bkms/index.html 
        
    ">Sphinx overview</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../sphinx-bkms/getting-started/index.html 
        
    ">Getting started</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../sphinx-bkms/writing-rst/index.html 
        
    ">reSTructuredText Syntax</a>
            
            
        
    

                </ul>
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../ExtCollab/opensourcejira.html 
        
    ">Open Source Instance Hosting</a>
            
            
        
    

                </ul>
            
        
    

            </ul>
        </div>
    

      
        
         
        

    
        
            <div class="nav-item d-flex align-items-center"  >
                <a 
                    class="nav-link text-uppercase text-dark" href="
    
        
            
            ../IntelOutside/IntelOutside.html 
        
    ">
                    Community and Evangelism
                </a>
            </div>
       
    

      
        
         
        

    
    
        <div class="nav-item dropdown align-items-center d-flex">
            <button class="btn dropdown-toggle nav-item border-0 text-uppercase text-dark" type="button"
                data-bs-toggle="dropdown" data-toggle="dropdown">
                Open Source Projects
            </button>
            <ul class="dropdown-menu dropdown-menu-right border-0">
                
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../2023OESummit/presentations.html 
        
    ">OpenEcoSummit Keynotes, Tech Sessions</a>
            
            
        
    
        
            
                <a 
                   class="dropdown-item"  href="
    
        
            
            ../2023OESummit/videoPortal.html 
        
    ">Open Source Project Videos</a>
            
            
        
    

            </ul>
        </div>
    

      
      
        

    
    
        <div class="nav-item dropdown align-items-center d-flex">
            <button class="btn dropdown-toggle nav-item border-0 text-uppercase text-dark" type="button"
                data-bs-toggle="dropdown" data-toggle="dropdown">
                Quick Links
            </button>
            <ul class="dropdown-menu dropdown-menu-right border-0">
                
    
        
            
                <a target="_blank" 
                   class="dropdown-item"  href="
    
        
            https://intel.sharepoint.com/sites/Trade/SitePages/What-is-Subject-to-Export-Control.aspx
        
    ">Export Control</a>
            
            
        
    
        
            
                <a target="_blank" 
                   class="dropdown-item"  href="
    
        
            https://intel.sharepoint.com/sites/SWLC
        
    ">Software Legal Compliance</a>
            
            
        
    
        
            
                <a target="_blank" 
                   class="dropdown-item"  href="
    
        
            https://legal.intel.com/Trademarks/
        
    ">Trademark and Brands</a>
            
            
        
    
        
            
                <a target="_blank" 
                   class="dropdown-item"  href="
    
        
            https://intel.sharepoint.com/sites/sdl?e=1%3Aa6a73cc602ce42c1ad6a63170447ad70
        
    ">SDL Essentials Portal</a>
            
            
        
    
        
            
                <a target="_blank" 
                   class="dropdown-item"  href="
    
        
            https://intel.sharepoint.com/sites/ospdt/Lists/OSPDT%20Meeting%20Calendar/calendar.aspx
        
    ">Open Source PDT Meeting Calender</a>
            
            
        
    
        
            <div class="dropdown-divider"></div>
        
    
        
            
                <a target="_blank" 
                   class="dropdown-item"  href="
    
        
            https://circuitplus.intel.com/channels/5606468
        
    ">Open Ecosystem Circuit+ Channel</a>
            
            
        
    
        
            
                <a target="_blank" 
                   class="dropdown-item"  href="
    
        
            https://open.intel.com
        
    ">Open Ecosystem - Public Website</a>
            
            
        
    
        
            
                <a target="_blank" 
                   class="dropdown-item" title="Featuring the projects and people who work to combine Intel's unique strengths in hardware with a commitment to a strong, open ecosystem." href="
    
        
            https://intel.sharepoint.com/sites/openinnovationseries
        
    ">Open Source Innovations Meetups</a>
            
            
        
    
        
            
                <a target="_blank" 
                   class="dropdown-item"  href="
    
        
            https://openatintel.podbean.com/
        
    ">Open@Intel Podcasts</a>
            
            
        
    
        
            <div class="dropdown-divider"></div>
        
    
        
            
                <a target="_blank" 
                   class="dropdown-item"  href="
    
        
            https://grit.intel.com/
        
    ">Intel Library - Tech, Mkting, Biz Journals</a>
            
            
        
    

            </ul>
        </div>
    

      
      <div class="nav-item">
          <form class="bd-search d-flex align-items-center mr-1" action="../search.html" method="get">
  <!--i class="icon fas fa-search"></i-->
  <input type="search" class="form-control ml-1" name="q" id="search-input" placeholder="Search the site..." aria-label="Search the site..." autocomplete="off" >
</form>
      </div>

    </ul>
  </div>
</nav>




		</div>

        
        
    
    


	

    <div class="bd-container">
         
           
               <!-- Only show if we have sidebars configured, else just a small margin  -->
               <div class="bd-sidebar"><nav class="bd-links w-100" id="bd-docs-nav" aria-label="Main navigation">
  <div class="bd-toc-item active">
    <ul class="current nav bd-sidenav">
 <li class="toctree-l1 current active has-children">
  <a class="reference internal" href="Learning.html">
   Learning
  </a>
  <input checked="" class="toctree-checkbox" id="toctree-checkbox-1" name="toctree-checkbox-1" type="checkbox"/>
  <label for="toctree-checkbox-1">
   <i class="fas fa-chevron-down">
   </i>
  </label>
  <ul class="current">
   <li class="toctree-l2">
    <a class="reference internal" href="licensing/Licensingtraining.html">
     Licensing Training Classes
    </a>
   </li>
   <li class="toctree-l2 has-children">
    <a class="reference internal" href="Preparingtheproject.html">
     Preparing for an Open Source Project
    </a>
    <input class="toctree-checkbox" id="toctree-checkbox-2" name="toctree-checkbox-2" type="checkbox"/>
    <label for="toctree-checkbox-2">
     <i class="fas fa-chevron-down">
     </i>
    </label>
    <ul>
     <li class="toctree-l3">
      <a class="reference internal" href="Whatisopensource.html">
       What is Open Source Software?
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="community/code-of-conduct.html">
       Contributor Covenant Code of Conduct
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="licensing/Licensingtraining.html">
       Licensing Training Classes
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="Settinguptheteam.html">
       Setting Up the Team
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="Developingintheopen.html">
       Developing in the Open
      </a>
     </li>
    </ul>
   </li>
   <li class="toctree-l2 has-children">
    <a class="reference internal" href="Prelaunch.html">
     Pre-Launch Activities - Chronological
    </a>
    <input class="toctree-checkbox" id="toctree-checkbox-3" name="toctree-checkbox-3" type="checkbox"/>
    <label for="toctree-checkbox-3">
     <i class="fas fa-chevron-down">
     </i>
    </label>
    <ul>
     <li class="toctree-l3">
      <a class="reference internal" href="Strategicplanning.html">
       Strategic Planning
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="Creatingopengovernance.html">
       Creating an Openly Governed Project Governance Model
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="licensing/Licensing.html">
       Licensing Basics and Training
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="Opensourcelicensingreview.html">
       Open Source Software Licensing Review
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="projectmanagement/Projectmanagement.html">
       Project Management
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="Advocacymarketing.html">
       Advocacy and Marketing
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="Documentation.html">
       Documentation: Tips and Best Practices
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="Webpresence.html">
       Web Presence
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="Preparingaproject.html">
       Open Source Software Release Approval
      </a>
     </li>
    </ul>
   </li>
   <li class="toctree-l2">
    <a class="reference internal" href="Launch.html">
     Launching a Project
    </a>
   </li>
   <li class="toctree-l2 current active has-children">
    <a class="reference internal" href="Developmentandmaintenance.html">
     Development and Maintenance - Alphabetic
    </a>
    <input checked="" class="toctree-checkbox" id="toctree-checkbox-4" name="toctree-checkbox-4" type="checkbox"/>
    <label for="toctree-checkbox-4">
     <i class="fas fa-chevron-down">
     </i>
    </label>
    <ul class="current">
     <li class="toctree-l3">
      <a class="reference internal" href="Cicd.html">
       CI/CD Continuous Integration and Deployment
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="Documentation.html">
       Documentation: Tips and Best Practices
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="Issuemanagement.html">
       Issue Management
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="Releasestrategy.html">
       Release Strategy
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="Reviewsystem.html">
       Review System
      </a>
     </li>
     <li class="toctree-l3 current active">
      <a class="current reference internal" href="#">
       Security Vulnerability Handling
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="Cvesecuritymanagement.html">
       CVE Management of 3rd Party Components
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="Supplychainsecurity.html">
       Supply Chain Security
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="Testingstrategy.html">
       Testing Strategy
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="Webpresence.html">
       Web Presence
      </a>
     </li>
    </ul>
   </li>
   <li class="toctree-l2 has-children">
    <a class="reference internal" href="Community.html">
     Working with the Community
    </a>
    <input class="toctree-checkbox" id="toctree-checkbox-5" name="toctree-checkbox-5" type="checkbox"/>
    <label for="toctree-checkbox-5">
     <i class="fas fa-chevron-down">
     </i>
    </label>
    <ul>
     <li class="toctree-l3">
      <a class="reference internal" href="Communicationchannels.html">
       Communication Channels
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="Developeroutreach.html">
       Developer Outreach
      </a>
     </li>
     <li class="toctree-l3">
      <a class="reference internal" href="Developermeetups.html">
       Developer Meetups
      </a>
     </li>
    </ul>
   </li>
   <li class="toctree-l2">
    <a class="reference internal" href="Exitingaproject.html">
     Exiting an Open Source Project
    </a>
   </li>
  </ul>
 </li>
</ul>

  </div>
</nav>
               </div>
           
         

      <main class="bd-main">
            

                <div class="content-row h-100" >

                    <div class="bd-content">

                        <div class="bd-article-container">

                                
    
    


                        
                        
                            <div id="bodyRow" class="row" role="main">

                                
    
    


                                
                                
  <section id="security-vulnerability-handling">
<span id="security-vulnerability"></span><h1>Security Vulnerability Handling</h1>
<section id="your-roles-and-responsibilities">
<h2>Your Roles and Responsibilities</h2>
<p>Where and how to handle a security issue in open source projects can be
confusing.  Please review the <a class="reference external" href="https://wiki.ith.intel.com/x/cdtSbg">IPAS policy for open source security
vulnerability handling</a> and <a class="reference external" href="https://wiki.ith.intel.com/x/k6GxPg">SDL Guidance for Open Source and Co-development</a> to fully understand your role and responsibilities. A
developer training to help you better understand your individual role is
available <a class="reference download internal" download="" href="../_downloads/6914e5e1ce32c9c54fb835f2412d7dc0/OSS-Security-Vulnerability-Handling-Developer-Training.pdf"><code class="xref download docutils literal notranslate"><span class="pre">here</span></code></a>.</p>
<p>An internal mailing list - <a class="reference external" href="mailto:oss-security&#37;&#52;&#48;eclists&#46;intel&#46;com">oss-security<span>&#64;</span>eclists<span>&#46;</span>intel<span>&#46;</span>com</a> - is available if
you require assistance in either understanding your role and responsibilities,
or how to handle a vulnerability within a specific project or product.</p>
</section>
<section id="intel-owned-project-product-responsibilities">
<h2>Intel-Owned Project/Product Responsibilities</h2>
<p>If you are responsible for a public Intel-owned opensource project you must:</p>
<ul class="simple">
<li><p>Provide a public security policy that directs users to report security issues to <a class="reference external" href="mailto:secure&#37;&#52;&#48;intel&#46;com">secure<span>&#64;</span>intel<span>&#46;</span>com</a>.</p>
<ul>
<li><p>Intel owned projects hosted on GitHub, especially any projects in official Intel GitHub organizations, should include a default <a class="reference download internal" download="" href="../_downloads/92189d0c290b3eb504dbc4390edf19a6/security.md"><code class="xref download docutils literal notranslate"><span class="pre">security.md</span></code></a> file that directs users into IPAS to report any security issues found in that project. Please download the default <a class="reference download internal" download="" href="../_downloads/92189d0c290b3eb504dbc4390edf19a6/security.md"><code class="xref download docutils literal notranslate"><span class="pre">security.md</span></code></a> and include it in the root of your github repository.</p></li>
</ul>
</li>
<li><p>Report any security issues identified during development to <a class="reference external" href="mailto:secure&#37;&#52;&#48;intel&#46;com">secure<span>&#64;</span>intel<span>&#46;</span>com</a></p></li>
<li><p>You must work with  IPAS to disclose issues and mitigations to your users.</p></li>
<li><p><strong>EXCEPTION</strong>: Intel staging should refer third-parties to the community project the staging tree feeds into.</p></li>
</ul>
<p>If you consume opensource software in an Intel branded product you must:</p>
<ul class="simple">
<li><p>Ensure that the project is well maintained and can fix and merge issues in a timely way into a regular release cadence.</p></li>
<li><p>Ensure that the project(s) has a security issue handling policy that defines:</p>
<ul>
<li><p>How security issues will be reported to the project, and whether that method is private or public.</p></li>
<li><p>How issues will be disclosed to users, and on what timeline</p></li>
</ul>
</li>
<li><p>Report any security issues in projects you consume in released versions of your product to <a class="reference external" href="mailto:secure&#37;&#52;&#48;intel&#46;com">secure<span>&#64;</span>intel<span>&#46;</span>com</a></p></li>
<li><p><strong>NOTE</strong>: If you consume critical dependencies from poorly maintained projects without defined security processes, you may be required to either remove the dependency, or mitigate known security vulnerabilities directly within your project.</p></li>
</ul>
</section>
<section id="community-project-expectations">
<h2>Community Project Expectations</h2>
<p>Intel would like to see a minimal security vulnerability process in place for any upstream community project Intel creates or participates in.  That process would ideally include:</p>
<ul class="simple">
<li><p>A private channel for reporting security issues to the project</p></li>
<li><p>A defined timeline for public disclosure of the issue/patches starting from the initial report.</p></li>
<li><p>A defined security advisory publication and CVE process.</p>
<ul>
<li><p>Projects can request CVEs directly from <a class="reference external" href="https://cve.mitre.org/cve/request_id.html">MITRE</a></p></li>
<li><p>GitHub has a well-defined <a class="reference external" href="https://docs.github.com/en/code-security/security-advisories/creating-a-security-advisory">process for creating security advisories and CVEs</a></p></li>
<li><p>Security issues can be privately disclosed to common Linux distributions through the Openwall <a class="reference external" href="https://oss-security.openwall.org/wiki/mailing-lists/distros#how-to-use-the-lists">Operating system distribution security contact lists</a> if coordinated deployment is required before public disclosure.</p></li>
</ul>
</li>
</ul>
<p>An internal mailing list - <a class="reference external" href="mailto:oss-security&#37;&#52;&#48;eclists&#46;intel&#46;com">oss-security<span>&#64;</span>eclists<span>&#46;</span>intel<span>&#46;</span>com</a> - is available if you require assistance in either understanding your role and responsibilities, or how to handle a vulnerability within a specific project or product.</p>
<blockquote>
<div><hr></div></blockquote>
</section>
<section id="revision-history">
<h2>Revision History</h2>
<div class="line-block">
<div class="line">v1.0 Initial Release June 2023</div>
</div>
</section>
</section>


                            
                                
    
    


                            </div>
                        

                                
    
    


                        </div>

                      </div>

            		  
                      
                   		 

                      
                        <div class="bd-sidebar-secondary bd-toc">
                          




<div class="tocsection onthispage pt-5 pb-3">
    <i class="fas fa-list"></i> On this page
</div>


<nav id="bd-toc-nav">
    <ul class="visible nav section-nav flex-column">
 <li class="toc-h2 nav-item toc-entry">
  <a class="reference internal nav-link" href="#your-roles-and-responsibilities">
   Your Roles and Responsibilities
  </a>
 </li>
 <li class="toc-h2 nav-item toc-entry">
  <a class="reference internal nav-link" href="#intel-owned-project-product-responsibilities">
   Intel-Owned Project/Product Responsibilities
  </a>
 </li>
 <li class="toc-h2 nav-item toc-entry">
  <a class="reference internal nav-link" href="#community-project-expectations">
   Community Project Expectations
  </a>
 </li>
 <li class="toc-h2 nav-item toc-entry">
  <a class="reference internal nav-link" href="#revision-history">
   Revision History
  </a>
 </li>
</ul>

</nav>

                        </div>
                      

                    </div>
                      

            

      </main>

   </div>

  
    
    

  
  <script src="../_static/js/index.be7d3bbb2ef33a8344ce.js"></script>
<footer class="footer mt-5 mt-md-0">
  <div class="container">
    
    <div class="footer-item">
      


    


<div class="row mt-3">
    
    <div class="col">
        <div class="card border-0 m-0 bg-tranparent">
           <div class="card-body p-0">
               <h4 class="card-title">Our Organization</h4>
                    
                    <a 
                        class="nav-link" href="
    
        
            https://intel.sharepoint.com/sites/strategytoexecution/SitePages/Open.Intel.aspx
        
    ">Open Ecosystem Org</a>
                    
                    <a 
                        class="nav-link" href="
    
        
            https://intel.sharepoint.com/sites/strategytoexecution
        
    ">Strategy to Execution (S2E)</a>
                    
                    <a 
                        class="nav-link" href="
    
        
            https://intel.sharepoint.com/sites/SATG
        
    ">Office of the CTO & SATG</a>
                    
           </div>
       </div>
    </div>
    
    <div class="col">
        <div class="card border-0 m-0 bg-tranparent">
           <div class="card-body p-0">
               <h4 class="card-title">Contact Us</h4>
                    
                    <a 
                        class="nav-link" href="
    
        
            https://web.yammer.com/main/org/intel.com/groups/eyJfdHlwZSI6Ikdyb3VwIiwiaWQiOiIxMjczNzU0NDE5MiJ9/new
        
    ">Open Ecosystem or content queries</a>
                    
                    <a 
                        class="nav-link" href="
    
        
            mailto:stephen.e.ware@intel.com
        
    ">Broken links, failed pages...</a>
                    
           </div>
       </div>
    </div>
    

    <div class="col">
        <div class="card border-0 m-0 bg-tranparent">
           <div class="card-body p-0">
               <h4 class="card-title">Rate this page</h4>
               <select id="starrating" class="star-rating" 
                   onchange="(() => gtag('event', 'star_rating', { stars: document.getElementById('starrating').value}))()">
                   <option value="5">Excellent</option>
                   <option value="4">Very Good</option>
                   <option value="3">Average</option>
                   <option value="2">Poor</option>
                   <option value="1">Terrible</option>
               </select>
           </div>
       </div>
    </div>
</div>
    <script>
            var stars = new StarRating('.star-rating', {tooltip:false});
    </script>

    </div>
    
  </div>
</footer>
  </body>
</html>