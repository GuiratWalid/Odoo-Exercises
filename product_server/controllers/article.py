import logging

from odoo import http
from odoo.http import request


_logger = logging.getLogger(__name__)


class ArticleController(http.Controller):
    @http.route("/api/articles", type="json", auth="user", methods=["GET"])
    def get_articles(self):
        _logger.info("GET request received at /api/articles")
        try:
            articles = request.env["product.template"].search([("type", "=", "consu")])
            if not articles:
                _logger.warning("No consumable products found")
                return {
                    "status": 404,
                    "response": [],
                    "message": "No consumable products found",
                }

            articles_list = [
                {"id": article.id, "name": article.name} for article in articles
            ]
            _logger.info(f"Returning {len(articles_list)} consumable products")
            return {"status": 200, "response": articles_list, "message": "Success"}

        except Exception as e:
            _logger.error(f"Error in /api/articles: {e}")
            return {"status": 500, "response": [], "message": str(e)}

    @http.route(
        "/api/articles/<int:article_id>", type="json", auth="user", methods=["GET"]
    )
    def get_article_details(self, article_id):
        _logger.info(f"GET request received at /api/articles/{article_id}")
        try:
            article = request.env["product.template"].sudo().browse(article_id)
            if not article.exists():
                _logger.warning(f"Article with ID {article_id} not found")
                return {"status": 404, "response": {}, "message": "Article not found"}

            article_data = {
                "id": article.id,
                "name": article.name,
                "description": article.description_sale or "No description",
            }
            _logger.info(f"Returning details for article ID {article_id}")
            return {"status": 200, "response": article_data, "message": "Success"}

        except Exception as e:
            _logger.error(f"Error in /api/articles: {e}")
            return {"status": 500, "response": {}, "message": str(e)}
