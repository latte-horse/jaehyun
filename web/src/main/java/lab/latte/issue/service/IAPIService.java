package lab.latte.issue.service;

import java.util.List;
import java.util.Map;

import lab.latte.issue.model.TimelineVO;

public interface IAPIService<T, K, V> {

	public TimelineVO getLastTimeunit();
	public TimelineVO getTimeunitByTime(Map<K, V> map);
	public TimelineVO getTimeunitByPos(int pos);
	public List<T> getPastTimeline(Map<K, V> map);
	public List<T> getFutureTimeline(Map<K, V> map);
	
}
