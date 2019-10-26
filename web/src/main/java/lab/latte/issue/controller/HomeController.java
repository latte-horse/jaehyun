package lab.latte.issue.controller;

import java.util.Locale;
import java.util.Properties;

import javax.annotation.Resource;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

/**
 * Handles requests for the application home page.
 */
@Controller
public class HomeController {
	
	@SuppressWarnings("unused")
	private static final Logger logger = LoggerFactory.getLogger(HomeController.class);
	
	@Resource(name="envProperties")
	private Properties env;
	
	@RequestMapping(value = "/", method = RequestMethod.GET)
	public String home(Locale locale, Model model) {

		return "home";
	}
	
	@RequestMapping(value = "/3d-test", method = RequestMethod.GET)
	public String test3d(Locale locale, Model model) {
		
		return "3d-test";
	}
	
	@RequestMapping(value = "/main-test", method = RequestMethod.GET)
	public String mainTest(Locale locale, Model model) {
		
		return "main-test";
	}
	
	@RequestMapping(value = "/page-test", method = RequestMethod.GET)
	public String pageTest(Locale locale, Model model) {
		
		return "page-test";
	}

}
