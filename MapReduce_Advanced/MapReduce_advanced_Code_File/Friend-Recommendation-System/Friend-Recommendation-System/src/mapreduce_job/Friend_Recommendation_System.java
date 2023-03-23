package mapreduce_job;

import java.util.*;
import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;


/*** Apache Hadoop Import Files  ***/
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;



public class Friend_Recommendation_System {
	static public class friendCounts implements Writable {
		public Long userId;
		public int friend;

		public void readFields(DataInput in) throws IOException {
			userId = in.readLong();
			friend = in.readInt();
		}
		
		public void write(DataOutput out) throws IOException {
			out.writeLong(userId);
			out.writeInt(friend);
		}
		
		public friendCounts(Long userId, int friend) {
			this.userId = userId;
			this.friend = friend;
		}
		
		public friendCounts() {
			this(-1L, -1);
		}
		
	}

	
	public static class Map extends Mapper<LongWritable, Text, LongWritable, friendCounts> {
		public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
			String line[] = value.toString().split("\t");
			Long user = Long.parseLong(line[0]); 					
			List<Long> friendsList = new ArrayList<Long>(); 			
			if (line.length == 2) {
				StringTokenizer token = new StringTokenizer(line[1], ",");
				while (token.hasMoreTokens()) {
					Long friend = Long.parseLong(token.nextToken());
					friendsList.add(friend);
					context.write(new LongWritable(user), new friendCounts(friend, 1));  
				}
				
				
				for (int a = 0; a < friendsList.size(); a++) {
					for (int b = a + 1; b < friendsList.size(); b++) {
						context.write(new LongWritable(friendsList.get(a)), new friendCounts((friendsList.get(b)), 0));
						context.write(new LongWritable(friendsList.get(b)), new friendCounts((friendsList.get(a)), 0));
					}
				}
			}
		}
	}
	
	
	public static class Reduce extends Reducer<LongWritable, friendCounts, LongWritable, Text> {
		public void reduce(LongWritable key, Iterable<friendCounts> values, Context context)
				throws IOException, InterruptedException {
			final java.util.Map<Long, Integer> friendsMap = new HashMap<Long, Integer>();
			
			for (friendCounts value : values) {
				final Boolean isFriendAlready = (value.friend == 1);
				final Long recommendFrind = value.userId;
				
				
				
				if (isFriendAlready)
				{
					friendsMap.put(recommendFrind, 0);
				}
				else
				{
					if (friendsMap.containsKey(recommendFrind))
					{
						if (friendsMap.get(recommendFrind) != 0 )
						{
							friendsMap.put(recommendFrind, friendsMap.get(recommendFrind)+1);
						}
					}
					else
					{
						friendsMap.put(recommendFrind, 1);
					}
				}
				
			}
			
			friendsMap.values().removeAll(Collections.singleton(0));

			// Sorting all the Mutual friends using Tree Map
			java.util.SortedMap<Long, Integer> sortFriends = new TreeMap<Long, Integer>(new Comparator<Long>() {
				public int compare(Long key1, Long key2) {
					Integer value1 = friendsMap.get(key1);
					Integer value2 = friendsMap.get(key2);
					if (value1 > value2) {
						return -1;
					} else if (value1.equals(value2) && key1 < key2) {
						return -1;
					} else {
						return 1;
					}
				}
			});

			for (java.util.Map.Entry<Long, Integer> entry : friendsMap.entrySet()) {
				if (entry.getValue() != 0) {
					sortFriends.put(entry.getKey(), entry.getValue());
				}
			}

			Integer i = 0;
			String output = "";
			for (java.util.Map.Entry<Long, Integer> entry : sortFriends.entrySet()) {
				if (i == 0) {
					output = entry.getKey().toString();
				} else if (i < 10){
					output += "," + entry.getKey().toString();
				}
				++i;
			}
			context.write(key, new Text(output));
		}
	}

	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();

		Job job = new Job(conf, "FriendsRecommendation");
		job.setJarByClass(Friend_Recommendation_System.class);
		job.setOutputKeyClass(LongWritable.class);
		job.setOutputValueClass(friendCounts.class);
		job.setMapperClass(Map.class);
		job.setReducerClass(Reduce.class);
		job.setInputFormatClass(TextInputFormat.class);
		job.setOutputFormatClass(TextOutputFormat.class);

		FileSystem outFs = new Path(args[1]).getFileSystem(conf);
		outFs.delete(new Path(args[1]), true);

		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));

		job.waitForCompletion(true);
	}
}