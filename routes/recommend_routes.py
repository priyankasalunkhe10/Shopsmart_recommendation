from flask import Blueprint, request, jsonify
import numpy as np

def get_recommend_blueprint(
    knn_location, knn_purchase, similarity_matrix,
    location_vectorizer, product_vectorizer,
    user_item_matrix, df_product, df_customer, df_transaction
):
    recommend_bp = Blueprint('recommend', __name__)

    @recommend_bp.route('/recommend/location', methods=['GET'])
    def recommend_by_location():

        location = request.args.get('location')

        if not location:
            return jsonify({"error": "❌ Location is required"}), 400
        
        loc_vector = location_vectorizer.transform([location])
        distances, indices = knn_location.kneighbors(loc_vector, n_neighbors=6)
        similar_customers = df_customer.iloc[indices[0][1:]]['customer_id'].tolist()
        recommended_ids = (
            df_transaction[df_transaction['customer_id'].isin(similar_customers)]
            .sort_values(by='purchase_date', ascending=False)['product_id']
            .unique()
            [:5]
        )
        products = df_product[df_product['product_id'].isin(recommended_ids)][['product_id', 'name']].drop_duplicates()
        return jsonify(products.to_dict(orient='records'))

    @recommend_bp.route('/recommend/past_purchase', methods=['GET'])
    def recommend_by_purchase():

        product_id = request.args.get('product_id')

        if not product_id or product_id not in user_item_matrix.columns:
            return jsonify({"error": "❌ Valid product_id is required"}), 400
        
        product_vector = user_item_matrix.T.loc[[product_id]]
        distances, indices = knn_purchase.kneighbors(product_vector, n_neighbors=6)
        recommended_ids = user_item_matrix.columns[indices[0][1:]]
        products = df_product[df_product['product_id'].isin(recommended_ids)][['product_id', 'name']].drop_duplicates()
        return jsonify(products.to_dict(orient='records'))

    @recommend_bp.route('/recommend/similar_product', methods=['GET'])
    def recommend_similar_products():
        query = request.args.get('query')
        if not query:
            return jsonify({"error": "❌ Query is required"}), 400
        query_vec = product_vectorizer.transform([query])
        sim_scores = np.dot(similarity_matrix, query_vec.T).flatten()
        top_indices = sim_scores.argsort()[::-1][:5]
        recommended_products = df_product.iloc[top_indices][['product_id', 'name']].drop_duplicates()
        return jsonify(recommended_products.to_dict(orient='records'))

    return recommend_bp
