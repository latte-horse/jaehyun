package lab.latte.issue.controller;

import java.util.Map;
import java.util.Properties;

import javax.annotation.Resource;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import lab.latte.issue.model.TimelineVO;
import lab.latte.issue.service.IAPIService;


@Controller
public class APIsController {
	
	@SuppressWarnings("unused")
	private static final Logger logger = LoggerFactory.getLogger(APIsController.class);

	@Resource(name = "apiService")
	private IAPIService apiService;
	
	@Resource(name="envProperties")
	private Properties env;

	
	@RequestMapping(value = "/apis/getLastTimeline", method = RequestMethod.POST)
	@ResponseBody
	public TimelineVO getLastTimeline() {
		TimelineVO result = apiService.getLastTimeline();
		return result;	
	}
	
	@RequestMapping(value = "/apis/getTimelineByPos", method = RequestMethod.POST)
	@ResponseBody
	public TimelineVO getTimelineByPos(@RequestBody Map<String, Object> params) {
		
		int posNum = (Integer)params.get("pos");
		
		TimelineVO result = apiService.getTimelineByPos(posNum);
		return result;	
	}
}
