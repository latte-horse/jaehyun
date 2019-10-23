package lab.latte.issue.dao;

import lab.latte.issue.model.TimelineVO;

public interface ITimelineDAO {
	
	public TimelineVO getLastTimeline();
	public TimelineVO getTimelineByPos(int pos);
//	public List<EmployeeVO> getEmployees(HashMap<String, Object> hm);
}
