public class OutputComputeClusters implements Serializable {

    private double[][] dependencies;

    public OutputComputeClusters() {
        this.dependencies = new double[0][0];
    }

    public OutputComputeClusters(double[][] dependencies) {
        this.dependencies = dependencies;
    }

    public double[][] getDependencies() {
        return dependencies;
    }
}