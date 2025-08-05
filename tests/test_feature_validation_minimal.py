"""
Test Minimal Feature Validation
"""

import pytest
from pyclarity.workflows.feature_validation_minimal import (
    SimpleFeature,
    ValidationScore,
    validate_feature_simple
)


class TestMinimalFeatureValidation:
    """Test minimal feature validation"""
    
    async def test_validate_simple_feature(self):
        """Test basic feature validation"""
        feature = SimpleFeature(
            name="Quick Search",
            description="Fast product search with autocomplete",
            user_benefit="Find products in seconds",
            complexity="low"
        )
        
        user_feedback = [
            "Search is too slow currently",
            "Can't find products easily",
            "Need better filters"
        ]
        
        result = await validate_feature_simple(feature, user_feedback)
        
        assert isinstance(result, ValidationScore)
        assert result.feature_name == "Quick Search"
        assert 0 <= result.score <= 1
        assert result.recommendation in ["Build", "Consider with modifications", "Don't build"]
        assert isinstance(result.reasons, list)
    
    async def test_high_value_feature(self):
        """Test high-value feature scores well"""
        feature = SimpleFeature(
            name="Security Fix",
            description="Critical security vulnerability patch",
            user_benefit="Protects user data from breaches",
            complexity="low"
        )
        
        result = await validate_feature_simple(feature, ["Security is critical"])
        
        # Security fixes should score high
        assert result.score >= 0.5
        assert "build" in result.recommendation.lower() or "Build" == result.recommendation
    
    async def test_low_value_feature(self):
        """Test low-value feature scores low"""
        feature = SimpleFeature(
            name="Fancy Animation",
            description="3D spinning logo on homepage",
            user_benefit="Looks cool",
            complexity="high"
        )
        
        result = await validate_feature_simple(feature, ["Performance is slow", "Too many animations"])
        
        # Low value high complexity should score lower
        assert result.score < 0.8  # Not necessarily very low due to AI reasoning
    
    def test_simple_feature_model(self):
        """Test SimpleFeature model"""
        feature = SimpleFeature(
            name="Test",
            description="Test feature",
            user_benefit="Testing"
        )
        assert feature.complexity == "medium"  # Default
        
        feature2 = SimpleFeature(
            name="Test2",
            description="Test feature 2",
            user_benefit="Testing 2",
            complexity="high"
        )
        assert feature2.complexity == "high"
    
    def test_validation_score_model(self):
        """Test ValidationScore model"""
        score = ValidationScore(
            feature_name="Test Feature",
            score=0.75,
            recommendation="Build",
            reasons=["High user value", "Low complexity"]
        )
        
        assert score.score == 0.75
        assert score.recommendation == "Build"
        assert len(score.reasons) == 2
        
        # Test score bounds
        with pytest.raises(ValueError):
            ValidationScore(
                feature_name="Bad",
                score=1.5,  # Too high
                recommendation="Build",
                reasons=[]
            )