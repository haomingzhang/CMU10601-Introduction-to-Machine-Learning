import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;

public class decisionTree {
	private static TreeNode root;
	public static String[] attrs;
	public static int colNum;
	public static int trainingNum;
	public static HashMap<String, String> posValue = new HashMap<String, String>();
	public static HashMap<String, String> negValue = new HashMap<String, String>();
	public static ArrayList<boolean[]> allTraining = new ArrayList<boolean[]>();
	public static int errorNum = 0;
	public static int testError = 0;
	
	public static double log2(double a){
		if (a <= 0){
			return 0;
		}
		return Math.log(a) / Math.log(2);
	}

	public static double mutualInformation(int leftP, int leftN, int rightP, int rightN) {

		double total = leftP + leftN + rightP + rightN;
		double totalPos = (leftP + rightP) / total;
		double totalNeg = (leftN + rightN) / total;
		double sourceH = - totalPos * log2(totalPos) - totalNeg * log2(totalNeg);

		//System.err.println("source H: " + sourceH);
		
		double left = leftP + leftN;
		double leftPos = leftP / left;
		double leftNeg = leftN / left;
		double leftH = - leftPos * log2(leftPos) - leftNeg * log2(leftNeg);

		double right = rightP + rightN;
		double rightPos = rightP / right;
		double rightNeg = rightN / right;
		double rightH = - rightPos * log2(rightPos) - rightNeg * log2(rightNeg);

		double mutual = sourceH - left / total * leftH - right / total * rightH;
		return mutual;
	}
	
	public static int[] ifSplitNode(ArrayList<Integer> trainingID, int attrID){//lp,ln,rp,rn
		int[] result = new int[4];
		int leftPos = 0;
		int leftNeg = 0;
		int rightPos = 0;
		int rightNeg = 0;
		
		for (int id : trainingID){
			if (allTraining.get(id)[attrID]){//left
				if (allTraining.get(id)[colNum-1]){//pos label
					leftPos++;
				} else {
					leftNeg++;
				}
			} else {//right
				if (allTraining.get(id)[colNum-1]){//pos label
					rightPos++;
				} else {
					rightNeg++;
				}
			}
		}
		result[0] = leftPos;
		result[1] = leftNeg;
		result[2] = rightPos;
		result[3] = rightNeg;
		
		return result;
		
	}

	/*
	 * 
	 */
	
	
	/*
	public static void endNode(TreeNode parent){
		System.err.println("make the children of this node leaves : " + attrs[parent.getAttrID()]);

		//int[] lr = ifSplitNode(parent.getTrainingID(), parent.getAttrID());
		int leftPos = parent.getLeftPos();
		int leftNeg = parent.getLeftNeg();
		int rightPos = parent.getRightPos();
		int rightNeg = parent.getRightNeg();
		
		if (leftPos > leftNeg){//judge as pos
			parent.setLeft(new TreeNode(true));
		} else {//judge as neg
			parent.setLeft(new TreeNode(false));
		}
		
		if (rightPos > rightNeg){
			parent.setRight(new TreeNode(true));
		} else {
			parent.setRight(new TreeNode(false));
		}
	}
	*/
	/*
	public static void endNode(TreeNode node){
		
		//System.err.println("make this node a leaf : " );
		node.makeLeaf(node.getTotalPos() > node.getTotalNeg());
		
		
	}
	*/
	
	public static TreeNode createRoot(){
		ArrayList<Integer> trainingID = new ArrayList<Integer>();
		for (int i=0; i<trainingNum; i++){
			trainingID.add(i);
		}
		
		//find the the attr which maximizes mutual information
		double max = 0d;
		int maxID = -1;
		int[] maxLR = null;
		for (int attrID=0; attrID < colNum-1; attrID++){
			int[] lr = ifSplitNode(trainingID, attrID);
			//System.err.println("lr: " + lr[0] + " " + lr[1] + " " + lr[2] + " " + lr[3]);
			double mutualInfo = mutualInformation(lr[0], lr[1], lr[2], lr[3]);
			//System.err.println("mutualInfo: " + mutualInfo);
			if (mutualInfo > max){
				max = mutualInfo;
				maxID = attrID;
				maxLR = lr;
			}
		}
		
		ArrayList<Integer> remainedAttrs = new ArrayList<Integer>(5);
		for (int attrID=0; attrID < colNum-1; attrID++){
			if(attrID != maxID){
				remainedAttrs.add(attrID);
			}
		}
		
		//System.err.println("Max Attr ID : " + maxID);// + "Root node is: " + attrs[maxID]);
		
		//split the node using this attr
		TreeNode ret = new TreeNode(maxID, maxLR[0]+maxLR[2], maxLR[1]+maxLR[3], 1, trainingID, remainedAttrs, false);
		ret.setLeftPos(maxLR[0]);
		ret.setLeftNeg(maxLR[1]);
		ret.setRightPos(maxLR[2]);
		ret.setRightNeg(maxLR[3]);
		
		return ret;
	}
	
	public static TreeNode createChild (TreeNode parent, ArrayList<Integer> trainingID, int totalPos, int totalNeg){
		
		//System.err.println("create child for :" + attrs[parent.getAttrID()]);
		
		ArrayList<Integer> remained = new ArrayList<Integer>();
		
		double max = 0d;
		int maxID = -1;
		int[] maxLR = null;
		for (int attrID : parent.getRemainedAttr()) {
			int[] lr = ifSplitNode(trainingID, attrID);
			double mutualInfo = mutualInformation(lr[0], lr[1], lr[2], lr[3]);
			if (mutualInfo >= 0.1 && mutualInfo > max) {
				max = mutualInfo;
				maxID = attrID;
				maxLR = lr;
			}
		}
		
		if (maxID == -1){// make this node leaf
			TreeNode node = new TreeNode(totalPos, totalNeg);
			
			node.makeLeaf(node.getTotalPos() > node.getTotalNeg());
			if (node.judge){
				errorNum += node.getTotalNeg();
			} else {
				errorNum += node.getTotalPos();
			}
			//System.err.println(errorNum);
			return node;
			
		}
		
		for (int attrID : parent.getRemainedAttr()){
			if (attrID != maxID){
				remained.add(attrID);
			}
		}
		
		TreeNode child = new TreeNode(maxID, totalPos, totalNeg, parent.getHeight() + 1, trainingID, remained, false);
		child.setLeftPos(maxLR[0]);
		child.setLeftNeg(maxLR[1]);
		child.setRightPos(maxLR[2]);
		child.setRightNeg(maxLR[3]);
		return child;
	}
	
	
	public static void splitRoot(TreeNode parent){
		/*
		if (parent.getRemainedAttr().size() == 0){// all attrs have been used
			
			TreeNode left = new TreeNode(parent.getLeftPos(), parent.getLeftNeg());
			parent.setLeft(left.makeLeaf(left.getTotalPos() > left.getTotalNeg()));
			
			TreeNode right = new TreeNode(parent.getRightPos(), parent.getRightNeg());
			parent.setRight(right.makeLeaf(right.getTotalPos() > right.getTotalNeg()));
			return;
		}
		*/

		ArrayList<Integer> leftTrainingID = new ArrayList<Integer>();
		ArrayList<Integer> rightTrainingID = new ArrayList<Integer>();
		
		
		for (int trainID : parent.getTrainingID()){
			if (allTraining.get(trainID)[parent.getAttrID()]){//left
				leftTrainingID.add(trainID);
			} else {
				rightTrainingID.add(trainID);
			}
		}
			
			
		// find the the attr which maximizes mutual information
		parent.setLeft(createChild(parent, leftTrainingID, parent.getLeftPos(), parent.getLeftNeg()));
		parent.setRight(createChild(parent, rightTrainingID, parent.getRightPos(), parent.getRightNeg()));
		
	}
	
	public static void finishSplit(TreeNode parent){
		// left leaf
		TreeNode left = new TreeNode(parent.getLeftPos(), parent.getLeftNeg());
		parent.setLeft(left.makeLeaf(left.getTotalPos() > left.getTotalNeg()));
		
		if (left.judge){
			errorNum += left.getTotalNeg();
		} else {
			errorNum += left.getTotalPos();
		}
		
		//System.err.println(attrs[parent.getAttrID()] + " leftPos " + parent.getLeftPos() + " leftNeg " + parent.getLeftNeg() +" left child : " + left.judge);
		
		
		// right leaf
		TreeNode right = new TreeNode(parent.getRightPos(), parent.getRightNeg());
		parent.setRight(right.makeLeaf(right.getTotalPos() > right.getTotalNeg()));
		
		if (right.judge){
			errorNum += right.getTotalNeg();
		} else {
			errorNum += right.getTotalPos();
		}
		
		//System.err.println(attrs[parent.getAttrID()] + " rightPos " + parent.getRightPos() + " rightNeg " + parent.getRightNeg() + " right child : " + right.judge);
	}

	public static void train(String trainFile) {
		try {
			FileReader fr = new FileReader(trainFile);
			BufferedReader br = new BufferedReader(fr);
			String line = null;
			int count = 0;
			HashMap<String, Integer> labels = new HashMap<String, Integer>();

			
			ArrayList<HashMap<String, Integer>> allMap;

			while ((line = br.readLine()) != null) {

				// skip the first line
				if (count == 0) {
					attrs = line.split(",");
					colNum = attrs.length;
					count++;
					continue;
				}

				// training data
				String[] words = line.split(",");
				String label = words[words.length - 1];
				boolean[] isPos = new boolean[words.length];

				// store pos and neg values of all attrs
				for (int i = 0; i < words.length - 1; i++) {
					if (!posValue.containsKey(attrs[i])) {
						posValue.put(attrs[i], words[i]);
					} else if(!negValue.containsKey(attrs[i]) && !posValue.get(attrs[i]).equals(words[i])){
						negValue.put(attrs[i], words[i]);
					}
				}

				// store training data

				for (int i = 0; i < words.length - 1; i++) {
					isPos[i] = (words[i].equals(posValue.get(attrs[i])));
				}
				isPos[words.length - 1] = (label.equals("democrat") || label.equals("A") || label.equals("yes"));
				
				//System.err.println(isPos[0] + " " + isPos[1] + " " + isPos[2]);
				
				allTraining.add(isPos);

				count++;
			}

			count--;

			trainingNum = count;
			br.close();
			fr.close();
			//System.err.println("negValue:" + negValue.toString());
			//System.err.println("trainNum: " + trainingNum);
			
			
			root = createRoot();
			System.out.println("[" + root.getTotalPos() + "+/" + root.getTotalNeg() + "-]");
			splitRoot(root);
			
			//root-left
			String attr = attrs[root.getAttrID()];
			System.out.println(attr + " = " + posValue.get(attr) + ": [" + root.getLeftPos() + "+/" + root.getLeftNeg() + "-]");
			
			if (!root.getLeft().isLeaf){
				TreeNode left = root.getLeft();
				finishSplit(root.getLeft());
				//left-left
				String attrL = attrs[root.getLeft().getAttrID()];
				System.out.println("| " + attrL + " = " + posValue.get(attrL) + ": [" + left.getLeftPos() + "+/" + left.getLeftNeg() + "-]");
				//left-right
				System.out.println("| " + attrL + " = " + negValue.get(attrL) + ": [" + left.getRightPos() + "+/" + left.getRightNeg() + "-]");
			} else {
				//System.err.println("root left child is leaf : " + root.getLeft().judge + " Pos: " + root.getLeftPos() + " Neg: " + root.getLeftNeg());
			}
			
			//root-right
			System.out.println(attr + " = " + negValue.get(attr) + ": [" + root.getRightPos() + "+/" + root.getRightNeg() + "-]");
			

			
			
			if (!root.getRight().isLeaf){
				TreeNode right = root.getRight();
				//System.err.println("root right child is : " + attrs[root.getRight().getAttrID()] + " Pos: " + root.getRightPos() + " Neg: " + root.getRightNeg());
				finishSplit(root.getRight());
				//right-left
				String attrR = attrs[root.getLeft().getAttrID()];
				System.out.println("| " + attrR + " = " + posValue.get(attrR) + ": [" + right.getLeftPos() + "+/" + right.getLeftNeg() + "-]");
				//right-right
				System.out.println("| " + attrR + " = " + negValue.get(attrR) + ": [" + right.getRightPos() + "+/" + right.getRightNeg() + "-]");
			} else {
				//System.err.println("root right child is leaf : " + root.getRight().judge + " Pos: " + root.getRightPos() + " Neg: " + root.getRightNeg());
			}
			
			System.out.println("error(train): " + ((double)errorNum / (double)trainingNum));
			
			
			
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public static void test(String testFile){
		try {
			FileReader fr = new FileReader(testFile);
			BufferedReader br = new BufferedReader(fr);
			String line = null;
			int count = 0;
			
			
			while ((line = br.readLine()) != null) {
				if (count == 0){
					count++;
					continue;
				}
				String[] words = line.split(",");
				String label = words[words.length-1];
				boolean[] isPos = new boolean[words.length];
				for (int i = 0; i < words.length - 1; i++) {
					isPos[i] = (words[i].equals(posValue.get(attrs[i])));
				}
				isPos[words.length - 1] = (label.equals("democrat") || label.equals("A") || label.equals("yes"));
				
				TreeNode current = root;
				while (!current.isLeaf){
					if (isPos[current.getAttrID()]){
						current = current.getLeft();
					} else {
						current = current.getRight();
					}
				}
				
				//System.err.println(current.judge + "" + isPos[words.length-1]);
				
				if (current.judge != isPos[words.length-1]){
					testError++;
				}
				count++;
			}
			count--;
			
			br.close();
			fr.close();
			
			System.out.println("error(test): " + ((double)testError / (double)count));
			
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args) {

		train(args[0]);
		test(args[1]);
	}
}