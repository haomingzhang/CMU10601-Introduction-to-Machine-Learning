import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

/*
 * Compute entropy and error
 */
public class inspect{
	
	public static void main(String[] args){
		try {
			FileReader fr = new FileReader(args[0]);
			BufferedReader br = new BufferedReader(fr);
			String line = null;
			int count = 0;
			HashMap<String, Integer> labels = new HashMap<String, Integer>();
			
			while ((line = br.readLine()) != null){
				
				//skip the first line
				if (count == 0){
					count++;
					continue;
				}
				String[] words = line.split(",");
				String label = words[words.length-1];
				//System.out.println(label);
				if (labels.containsKey(label)){
					labels.put(label, labels.get(label) + 1);
				} else {
					labels.put(label, 1);
				}
				
				count++;
			}
			
			count--;
			double entropy = 0;
			int majority = 0;
			for (String key : labels.keySet()){
				if (labels.get(key) > majority){
					majority = labels.get(key);
				}
				double p = ((double)labels.get(key)) / ((double)count);
				entropy -= p * Math.log(p) / Math.log(2);
				
				//System.out.println(labels.get(key));
			}
			
			double errorRate = 1 - ((double) majority) / ((double) count);
			//System.out.println(count);
			
			System.out.println("entropy: " + entropy);
			System.out.println("error: " + errorRate);
			
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}