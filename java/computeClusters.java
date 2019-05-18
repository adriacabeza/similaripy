    public double cosineSimilarity(Map<String, Map<String, Double>> res, String a, String b) {
        double cosine=0.0;
        Map<String,Double> wordsA=res.get(a);
        Map<String,Double> wordsB=res.get(b);
        Set<String> intersection= new HashSet<String>(wordsA.keySet());
        intersection.retainAll(wordsB.keySet());
        for (String s: intersection) {
            Double forA=wordsA.get(s);
            Double forB=wordsB.get(s);
            cosine+=(forA-forB)*(forA-forB);
        }
        return cosine;
    }


public OutputComputeClusters computeClusters(String organization, double input_threshold, InputComputeClusters input) throws BadRequestException, NotFoundException, InternalErrorException {
    if (input.getRequirements().size() < 10) throw new BadRequestException("At a minimum there must be 10 entry requirements");

    show_time("start computeClusters");

    CosineSimilarity cosineSimilarity = CosineSimilarity.getInstance();

    Model model = null;
    try {
        model = modelDAO.getModel(organization);
    } catch (SQLException e) {
        throw new InternalErrorException("Error while loading the model from the database");
    }

    List<String> requirements = input.getRequirements();
    int max_size = requirements.size();
    double[][] matrix = new double[max_size][max_size];

    for (int i = 0; i < max_size; ++i) {
        String req1 = requirements.get(i);
        if (!model.getDocs().containsKey(req1)) throw new BadRequestException("The loaded model does not contain a requirement with id " + req1);
        for (int j = 0; j < max_size; ++j) {
            if (j == i) {
                matrix[i][j] = 1;
                matrix[j][i] = 1;
            } else {
                if (j > i) {
                    String req2 = requirements.get(j);
                    if (!model.getDocs().containsKey(req2)) throw new BadRequestException("The loaded model does not contain a requirement with id " + req2);
                    double score = cosineSimilarity(model.getDocs(), req1, req2);
                    matrix[i][j] = score;
                    matrix[j][i] = score;
                }
            }
        }
    }

    return new OutputComputeClusters(matrix);
}