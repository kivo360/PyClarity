"""
Test Feature Validation Pipeline
"""

import pytest
from pyclarity.workflows.feature_validation_simple import (
    FeatureToValidate,
    ValidationResult,
    SimpleFeatureValidator
)


class TestFeatureValidation:
    """Test feature validation functionality"""
    
    @pytest.fixture
    def validator(self):
        """Create validator instance"""
        return SimpleFeatureValidator()
    
    @pytest.fixture
    def sample_feature(self):
        """Sample feature to validate"""
        return FeatureToValidate(
            name="Quick Checkout",
            description="One-click checkout with saved payment methods",
            user_story="As a returning customer, I want to checkout quickly so I don't abandon my cart",
            complexity="medium"
        )
    
    @pytest.fixture
    def sample_personas(self):
        """Sample user personas"""
        return [
            {
                "name": "Busy Professional",
                "viewpoint": "I value my time above all",
                "needs": ["Speed", "Convenience", "Security"],
                "concerns": ["Data security", "Accidental purchases"]
            },
            {
                "name": "Cautious Shopper",
                "viewpoint": "I want to review everything before buying",
                "needs": ["Transparency", "Control", "Confirmation"],
                "concerns": ["Hidden fees", "Wrong items", "No review step"]
            }
        ]
    
    async def test_feature_validation_basic(self, validator, sample_feature, sample_personas):
        """Test basic feature validation"""
        result = await validator.validate_feature(sample_feature, sample_personas)
        
        assert isinstance(result, ValidationResult)
        assert result.feature_name == "Quick Checkout"
        assert 0 <= result.overall_score <= 1
        assert result.recommendation in ["Build", "Modify", "Reject"]
        assert result.priority in ["P0", "P1", "P2", "P3"]
        assert len(result.key_insights) > 0
        assert len(result.risks) > 0
    
    async def test_high_value_feature(self, validator):
        """Test validation of high-value feature"""
        feature = FeatureToValidate(
            name="Security Enhancement",
            description="Two-factor authentication for all accounts",
            user_story="As a user, I want my account secured so my data is protected",
            complexity="low"
        )
        
        personas = [
            {
                "name": "Security-Conscious User",
                "needs": ["Data protection", "Account security"],
                "concerns": ["Complexity", "Login friction"]
            }
        ]
        
        result = await validator.validate_feature(feature, personas)
        
        # Security features should score high
        assert result.overall_score >= 0.6
        assert result.recommendation in ["Build", "Modify"]
    
    async def test_low_value_feature(self, validator):
        """Test validation of low-value feature"""
        feature = FeatureToValidate(
            name="Animated Avatars",
            description="Fun animated avatars for user profiles",
            user_story="As a user, I want animated avatars so my profile looks cool",
            complexity="high"
        )
        
        personas = [
            {
                "name": "Practical User",
                "viewpoint": "I just want core functionality",
                "needs": ["Performance", "Reliability"],
                "concerns": ["Distractions", "Load time"]
            }
        ]
        
        result = await validator.validate_feature(feature, personas)
        
        # Low-value high-complexity features should score low
        assert result.overall_score < 0.6
        assert result.priority in ["P2", "P3"]
    
    async def test_multiple_perspectives(self, validator):
        """Test with many user perspectives"""
        feature = FeatureToValidate(
            name="Mobile App",
            description="Native mobile application for iOS and Android",
            user_story="As a mobile user, I want a native app so I can shop on the go",
            complexity="high"
        )
        
        personas = [
            {"name": "Mobile-First User", "needs": ["Mobile access", "Offline mode"]},
            {"name": "Desktop User", "needs": ["Full features", "Large screen"]},
            {"name": "Tech Novice", "needs": ["Simplicity", "Help guides"]},
            {"name": "Power User", "needs": ["Advanced features", "Customization"]}
        ]
        
        result = await validator.validate_feature(feature, personas)
        
        assert isinstance(result, ValidationResult)
        assert len(result.key_insights) > 0
        # With diverse perspectives, should get moderate score
        assert 0.3 <= result.overall_score <= 0.8
    
    def test_feature_model_validation(self):
        """Test feature model validation"""
        # Valid feature
        feature = FeatureToValidate(
            name="Test Feature",
            description="A test feature",
            user_story="As a tester, I want to test",
            complexity="low"
        )
        assert feature.name == "Test Feature"
        assert feature.complexity == "low"
        
        # Default complexity
        feature2 = FeatureToValidate(
            name="Another Feature",
            description="Another test",
            user_story="As a user, I want this"
        )
        assert feature2.complexity == "medium"
    
    def test_validation_result_model(self):
        """Test validation result model"""
        result = ValidationResult(
            feature_name="Test",
            overall_score=0.75,
            recommendation="Build",
            key_insights=["High user value", "Low complexity"],
            risks=["Technical debt"],
            priority="P1"
        )
        
        assert result.overall_score == 0.75
        assert result.recommendation == "Build"
        assert len(result.key_insights) == 2
        assert len(result.risks) == 1
        assert result.priority == "P1"