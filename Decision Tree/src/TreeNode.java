import java.util.ArrayList;


public class TreeNode {
		private int attrID;
		private TreeNode left;
		private TreeNode right;
		private String leftValue;
		private String rightValue;
		private int totalPos;
		private int totalNeg;
		private int leftPos;
		private int leftNeg;
		private int rightPos;
		private int rightNeg;
		private int height;
		private ArrayList<Integer> trainingID;
		private ArrayList<Integer> remainedAttr;
		public boolean isLeaf;
		public boolean judge;
		public TreeNode makeLeaf(boolean judge){
			this.judge = judge;
			this.isLeaf = true;
			this.left = null;
			this.right = null;
			return this;
		}
		
		
		public TreeNode(){};
		
		public TreeNode(int totalPos, int totalNeg){
			this.setTotalPos(totalPos);
			this.setTotalNeg(totalNeg);
		}
		
		public TreeNode(int attrID, int totalPos, int totalNeg, int height, ArrayList<Integer> trainingID, ArrayList<Integer> remainedAttr,
				boolean isLeaf) {
			this.attrID = attrID;
			this.setTotalNeg(totalNeg);
			this.setTotalPos(totalPos);
			this.setHeight(height);
			this.setTrainingID(trainingID);
			this.setRemainedAttr(remainedAttr);
			this.isLeaf = isLeaf;
			this.setLeft(null);
			this.setRight(null);
			this.setLeftValue(null);
			this.setRightValue(null);

		}

		
		
		public int getAttrID(){
			return this.attrID;
		}
		
		// only valid for leaf
		public boolean classify() throws Exception {
			if (!isLeaf) {
				throw new Exception("Classify is only valid for leaf nodes!");
			}
			return false;
		}



		public TreeNode getLeft() {
			return left;
		}

		public void setLeft(TreeNode left) {
			this.left = left;
		}

		public TreeNode getRight() {
			return right;
		}

		public void setRight(TreeNode right) {
			this.right = right;
		}

		public String getLeftValue() {
			return leftValue;
		}

		public void setLeftValue(String leftValue) {
			this.leftValue = leftValue;
		}

		public String getRightValue() {
			return rightValue;
		}

		public void setRightValue(String rightValue) {
			this.rightValue = rightValue;
		}

		public int getTotalPos() {
			return totalPos;
		}

		public void setTotalPos(int totalPos) {
			this.totalPos = totalPos;
		}

		public int getTotalNeg() {
			return totalNeg;
		}

		public void setTotalNeg(int totalNeg) {
			this.totalNeg = totalNeg;
		}

		public int getLeftPos() {
			return leftPos;
		}

		public void setLeftPos(int leftPos) {
			this.leftPos = leftPos;
		}

		public int getLeftNeg() {
			return leftNeg;
		}

		public void setLeftNeg(int leftNeg) {
			this.leftNeg = leftNeg;
		}

		public int getRightPos() {
			return rightPos;
		}

		public void setRightPos(int rightPos) {
			this.rightPos = rightPos;
		}

		public int getRightNeg() {
			return rightNeg;
		}

		public void setRightNeg(int rightNeg) {
			this.rightNeg = rightNeg;
		}

		public int getHeight() {
			return height;
		}

		public void setHeight(int height) {
			this.height = height;
		}

		public ArrayList<Integer> getTrainingID() {
			return trainingID;
		}

		public void setTrainingID(ArrayList<Integer> trainingID) {
			this.trainingID = trainingID;
		}

		public ArrayList<Integer> getRemainedAttr() {
			return remainedAttr;
		}

		public void setRemainedAttr(ArrayList<Integer> remainedAttr) {
			this.remainedAttr = remainedAttr;
		}
	}