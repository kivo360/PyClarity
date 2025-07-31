"""
Tests for Journey Orchestration Intelligence Tool

Tests cover:
- Journey decomposition and analysis
- Multi-actor perspective synthesis
- Emotional journey calibration
- Health monitoring and diagnostics
- Optimization strategy generation
"""

import pytest
import asyncio
from typing import Dict, List
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch

# Assuming the journey orchestration module structure
from src.cognitive_tools.journey_orchestration import (
    JourneyOrchestrationIntelligence,
    JourneyDecompositionEngine,
    MultiActorPerspectiveSynthesizer,
    JourneyHealthMonitor,
    EmotionalJourneyCalibrator,
    JourneyOptimizationStrategist,
    JourneyContext,
    Actor,
    Touchpoint,
    JourneyHealth,
    EmotionalState,
    OptimizationStrategy
)


class TestJourneyDecompositionEngine:
    """Test journey decomposition functionality"""
    
    @pytest.fixture
    def decomposition_engine(self):
        return JourneyDecompositionEngine()
    
    @pytest.fixture
    def sample_journey_narrative(self):
        return {
            'title': 'Customer Onboarding Journey',
            'description': 'New customer signs up, verifies identity, sets up account, makes first transaction',
            'actors': ['customer', 'support_agent', 'automated_system'],
            'duration': '7 days',
            'channels': ['web', 'mobile', 'email', 'phone']
        }
    
    async def test_extract_touchpoints(self, decomposition_engine, sample_journey_narrative):
        """Test touchpoint extraction from journey narrative"""
        result = await decomposition_engine.extract_touchpoints(sample_journey_narrative)
        
        assert 'touchpoints' in result
        assert len(result['touchpoints']) >= 4  # At least 4 major touchpoints
        
        # Verify touchpoint structure
        for touchpoint in result['touchpoints']:
            assert 'id' in touchpoint
            assert 'name' in touchpoint
            assert 'actors' in touchpoint
            assert 'channels' in touchpoint
            assert 'duration' in touchpoint
    
    async def test_identify_actors(self, decomposition_engine, sample_journey_narrative):
        """Test actor identification and role mapping"""
        result = await decomposition_engine.identify_actors(sample_journey_narrative)
        
        assert 'actors' in result
        assert len(result['actors']) == 3
        
        # Check actor profiles
        customer = next(a for a in result['actors'] if a['id'] == 'customer')
        assert customer['role'] == 'primary'
        assert 'goals' in customer
        assert 'pain_points' in customer
    
    async def test_map_dependencies(self, decomposition_engine, sample_journey_narrative):
        """Test dependency mapping between touchpoints"""
        touchpoints = await decomposition_engine.extract_touchpoints(sample_journey_narrative)
        dependencies = await decomposition_engine.map_dependencies(touchpoints['touchpoints'])
        
        assert 'dependency_graph' in dependencies
        assert 'critical_path' in dependencies
        assert 'parallel_paths' in dependencies
        
        # Verify critical path makes sense
        critical_path = dependencies['critical_path']
        assert len(critical_path) >= 3  # At least 3 steps in critical path
    
    async def test_identify_gaps(self, decomposition_engine):
        """Test gap identification in journey"""
        incomplete_journey = {
            'touchpoints': [
                {'id': 'signup', 'next': 'verification'},
                {'id': 'verification', 'next': 'dashboard'},
                # Missing setup step
                {'id': 'dashboard', 'next': 'transaction'}
            ]
        }
        
        gaps = await decomposition_engine.identify_gaps(incomplete_journey)
        
        assert 'missing_touchpoints' in gaps
        assert 'broken_flows' in gaps
        assert len(gaps['missing_touchpoints']) > 0


class TestMultiActorPerspectiveSynthesizer:
    """Test multi-actor perspective analysis"""
    
    @pytest.fixture
    def perspective_synthesizer(self):
        return MultiActorPerspectiveSynthesizer()
    
    @pytest.fixture
    def sample_actors(self):
        return [
            Actor(
                id='customer',
                name='New Customer',
                type='primary',
                goals=['quick_setup', 'understand_features', 'feel_secure'],
                pain_points=['complex_forms', 'long_wait_times', 'unclear_instructions'],
                expectations={'response_time': '<5min', 'ease_of_use': 'high'}
            ),
            Actor(
                id='support_agent',
                name='Customer Support',
                type='service_provider',
                goals=['help_customer', 'resolve_quickly', 'maintain_quality'],
                pain_points=['system_limitations', 'unclear_customer_needs', 'time_pressure'],
                expectations={'tools_availability': 'high', 'customer_cooperation': 'medium'}
            )
        ]
    
    async def test_analyze_perspectives(self, perspective_synthesizer, sample_actors):
        """Test perspective analysis for each actor"""
        result = await perspective_synthesizer.analyze_perspectives(sample_actors)
        
        assert 'perspectives' in result
        assert len(result['perspectives']) == 2
        
        # Check perspective depth
        customer_perspective = result['perspectives']['customer']
        assert 'emotional_journey' in customer_perspective
        assert 'information_needs' in customer_perspective
        assert 'decision_points' in customer_perspective
        assert 'success_metrics' in customer_perspective
    
    async def test_identify_conflicts(self, perspective_synthesizer, sample_actors):
        """Test conflict identification between perspectives"""
        perspectives = await perspective_synthesizer.analyze_perspectives(sample_actors)
        conflicts = await perspective_synthesizer.identify_conflicts(perspectives['perspectives'])
        
        assert 'conflicts' in conflicts
        assert len(conflicts['conflicts']) > 0
        
        # Verify conflict structure
        for conflict in conflicts['conflicts']:
            assert 'actors' in conflict
            assert 'issue' in conflict
            assert 'severity' in conflict
            assert 'resolution_options' in conflict
    
    async def test_find_synergies(self, perspective_synthesizer, sample_actors):
        """Test synergy identification"""
        perspectives = await perspective_synthesizer.analyze_perspectives(sample_actors)
        synergies = await perspective_synthesizer.find_synergies(perspectives['perspectives'])
        
        assert 'synergies' in synergies
        assert 'shared_goals' in synergies
        assert 'complementary_capabilities' in synergies
        assert 'mutual_benefits' in synergies


class TestJourneyHealthMonitor:
    """Test journey health monitoring"""
    
    @pytest.fixture
    def health_monitor(self):
        return JourneyHealthMonitor()
    
    @pytest.fixture
    def sample_journey_metrics(self):
        return {
            'touchpoints': [
                {'id': 'signup', 'completion_rate': 0.85, 'avg_time': 300, 'satisfaction': 4.2},
                {'id': 'verification', 'completion_rate': 0.65, 'avg_time': 600, 'satisfaction': 3.1},
                {'id': 'setup', 'completion_rate': 0.45, 'avg_time': 900, 'satisfaction': 3.5},
                {'id': 'first_use', 'completion_rate': 0.78, 'avg_time': 120, 'satisfaction': 4.5}
            ],
            'overall_metrics': {
                'end_to_end_completion': 0.35,
                'avg_total_time': 1920,
                'nps_score': 32
            }
        }
    
    async def test_calculate_health_metrics(self, health_monitor, sample_journey_metrics):
        """Test health metric calculation"""
        health = await health_monitor.calculate_health_metrics(sample_journey_metrics)
        
        assert 'flow_efficiency' in health
        assert 'friction_index' in health
        assert 'dropout_risk' in health
        assert 'satisfaction_trajectory' in health
        assert 'value_delivery_rate' in health
        
        # Verify ranges
        assert 0 <= health['flow_efficiency'] <= 1
        assert 0 <= health['friction_index'] <= 1
        assert 0 <= health['dropout_risk'] <= 1
    
    async def test_diagnose_bottlenecks(self, health_monitor, sample_journey_metrics):
        """Test bottleneck detection"""
        diagnosis = await health_monitor.diagnose_bottlenecks(sample_journey_metrics)
        
        assert 'bottlenecks' in diagnosis
        assert len(diagnosis['bottlenecks']) > 0
        
        # Verification touchpoint should be identified as bottleneck
        verification_bottleneck = next(
            b for b in diagnosis['bottlenecks'] 
            if b['touchpoint'] == 'verification'
        )
        assert verification_bottleneck is not None
        assert verification_bottleneck['severity'] == 'high'
        assert 'causes' in verification_bottleneck
        assert 'recommendations' in verification_bottleneck
    
    async def test_predict_journey_failure(self, health_monitor, sample_journey_metrics):
        """Test journey failure prediction"""
        prediction = await health_monitor.predict_failure_points(sample_journey_metrics)
        
        assert 'failure_probability' in prediction
        assert 'high_risk_points' in prediction
        assert 'early_warning_signals' in prediction
        
        # Should identify setup as high risk due to low completion
        assert 'setup' in [p['touchpoint'] for p in prediction['high_risk_points']]


class TestEmotionalJourneyCalibrator:
    """Test emotional journey calibration"""
    
    @pytest.fixture
    def emotional_calibrator(self):
        return EmotionalJourneyCalibrator()
    
    @pytest.fixture
    def sample_emotional_data(self):
        return {
            'touchpoints': [
                {'id': 'signup', 'emotions': {'confidence': 0.8, 'frustration': 0.2, 'delight': 0.6}},
                {'id': 'verification', 'emotions': {'confidence': 0.4, 'frustration': 0.7, 'anxiety': 0.6}},
                {'id': 'setup', 'emotions': {'confidence': 0.5, 'frustration': 0.5, 'hope': 0.6}},
                {'id': 'success', 'emotions': {'confidence': 0.9, 'delight': 0.8, 'trust': 0.7}}
            ]
        }
    
    async def test_map_emotional_journey(self, emotional_calibrator, sample_emotional_data):
        """Test emotional journey mapping"""
        emotional_map = await emotional_calibrator.map_emotional_journey(sample_emotional_data)
        
        assert 'emotional_arc' in emotional_map
        assert 'peak_moments' in emotional_map
        assert 'valley_moments' in emotional_map
        assert 'emotional_volatility' in emotional_map
        
        # Verification should be identified as valley
        valleys = emotional_map['valley_moments']
        assert any(v['touchpoint'] == 'verification' for v in valleys)
    
    async def test_calibrate_interventions(self, emotional_calibrator, sample_emotional_data):
        """Test emotional intervention design"""
        emotional_map = await emotional_calibrator.map_emotional_journey(sample_emotional_data)
        interventions = await emotional_calibrator.design_interventions(emotional_map)
        
        assert 'interventions' in interventions
        assert len(interventions['interventions']) > 0
        
        # Should have intervention for verification frustration
        verification_intervention = next(
            i for i in interventions['interventions']
            if i['touchpoint'] == 'verification'
        )
        assert verification_intervention is not None
        assert 'type' in verification_intervention
        assert 'actions' in verification_intervention
        assert 'expected_impact' in verification_intervention


class TestJourneyOptimizationStrategist:
    """Test journey optimization strategies"""
    
    @pytest.fixture
    def optimization_strategist(self):
        return JourneyOptimizationStrategist()
    
    @pytest.fixture
    def sample_journey_analysis(self):
        return {
            'health_metrics': {
                'flow_efficiency': 0.45,
                'friction_index': 0.65,
                'satisfaction': 3.7
            },
            'bottlenecks': [
                {'touchpoint': 'verification', 'severity': 'high'},
                {'touchpoint': 'setup', 'severity': 'medium'}
            ],
            'emotional_valleys': [
                {'touchpoint': 'verification', 'primary_emotion': 'frustration'}
            ]
        }
    
    async def test_generate_optimization_strategies(self, optimization_strategist, sample_journey_analysis):
        """Test optimization strategy generation"""
        strategies = await optimization_strategist.generate_strategies(sample_journey_analysis)
        
        assert 'strategies' in strategies
        assert len(strategies['strategies']) >= 3  # At least 3 strategy types
        
        # Check strategy categories
        strategy_types = {s['type'] for s in strategies['strategies']}
        assert 'path_shortening' in strategy_types
        assert 'friction_reduction' in strategy_types
        assert 'experience_enhancement' in strategy_types
    
    async def test_prioritize_strategies(self, optimization_strategist, sample_journey_analysis):
        """Test strategy prioritization"""
        strategies = await optimization_strategist.generate_strategies(sample_journey_analysis)
        prioritized = await optimization_strategist.prioritize_strategies(
            strategies['strategies'],
            criteria={'impact': 0.4, 'effort': 0.3, 'risk': 0.3}
        )
        
        assert 'prioritized_strategies' in prioritized
        assert len(prioritized['prioritized_strategies']) > 0
        
        # First strategy should have highest score
        first_strategy = prioritized['prioritized_strategies'][0]
        assert 'priority_score' in first_strategy
        assert 'implementation_plan' in first_strategy
        assert 'expected_outcomes' in first_strategy
    
    async def test_simulate_optimization_impact(self, optimization_strategist):
        """Test optimization impact simulation"""
        strategy = OptimizationStrategy(
            type='path_shortening',
            actions=['remove_redundant_verification', 'parallel_processing'],
            touchpoints=['verification', 'setup'],
            expected_impact={'time_reduction': 0.3, 'completion_increase': 0.2}
        )
        
        current_metrics = {
            'avg_time': 1920,
            'completion_rate': 0.35,
            'satisfaction': 3.7
        }
        
        simulation = await optimization_strategist.simulate_impact(strategy, current_metrics)
        
        assert 'projected_metrics' in simulation
        assert 'confidence_interval' in simulation
        assert 'risk_factors' in simulation
        
        # Should show improvements
        assert simulation['projected_metrics']['avg_time'] < current_metrics['avg_time']
        assert simulation['projected_metrics']['completion_rate'] > current_metrics['completion_rate']


class TestIntegratedJourneyOrchestration:
    """Test integrated journey orchestration system"""
    
    @pytest.fixture
    def journey_orchestrator(self):
        return JourneyOrchestrationIntelligence()
    
    @pytest.fixture
    def sample_journey_context(self):
        return JourneyContext(
            domain='customer_experience',
            type='onboarding',
            actors=['customer', 'support', 'system'],
            constraints={'time': '7_days', 'budget': 'medium'},
            objectives=['conversion', 'satisfaction', 'efficiency']
        )
    
    async def test_full_journey_analysis(self, journey_orchestrator, sample_journey_context):
        """Test complete journey analysis pipeline"""
        analysis = await journey_orchestrator.analyze_journey(sample_journey_context)
        
        # Verify all components present
        assert 'decomposition' in analysis
        assert 'perspectives' in analysis
        assert 'health_assessment' in analysis
        assert 'emotional_profile' in analysis
        assert 'optimization_recommendations' in analysis
        
        # Verify integration
        assert analysis['optimization_recommendations']['strategies'][0]['addresses_bottlenecks']
        assert analysis['optimization_recommendations']['strategies'][0]['considers_emotions']
        assert analysis['optimization_recommendations']['strategies'][0]['multi_actor_impact']
    
    async def test_journey_monitoring(self, journey_orchestrator):
        """Test real-time journey monitoring"""
        # Setup monitoring
        monitor_id = await journey_orchestrator.start_monitoring('test_journey_001')
        
        # Simulate journey events
        events = [
            {'touchpoint': 'signup', 'actor': 'customer', 'status': 'completed', 'time': 280},
            {'touchpoint': 'verification', 'actor': 'customer', 'status': 'abandoned', 'time': 450}
        ]
        
        for event in events:
            await journey_orchestrator.record_event(monitor_id, event)
        
        # Get monitoring insights
        insights = await journey_orchestrator.get_monitoring_insights(monitor_id)
        
        assert 'real_time_health' in insights
        assert 'alerts' in insights
        assert 'recommended_interventions' in insights
        
        # Should alert on abandonment
        assert any(a['type'] == 'abandonment' for a in insights['alerts'])
    
    async def test_adaptive_optimization(self, journey_orchestrator, sample_journey_context):
        """Test adaptive optimization based on real-time data"""
        # Initial analysis
        initial_analysis = await journey_orchestrator.analyze_journey(sample_journey_context)
        
        # Simulate poor performance data
        performance_data = {
            'completion_rate': 0.25,  # Below expected
            'satisfaction': 3.2,       # Below target
            'friction_points': ['verification', 'complex_forms']
        }
        
        # Get adaptive recommendations
        adaptive_strategies = await journey_orchestrator.adapt_journey(
            sample_journey_context,
            performance_data
        )
        
        assert 'immediate_actions' in adaptive_strategies
        assert 'long_term_improvements' in adaptive_strategies
        assert 'experiment_suggestions' in adaptive_strategies
        
        # Should prioritize verification improvement
        immediate = adaptive_strategies['immediate_actions']
        assert any('verification' in action['target'] for action in immediate)


@pytest.mark.asyncio
class TestPerformanceAndScale:
    """Test performance and scalability"""
    
    async def test_large_journey_processing(self):
        """Test handling of complex journeys with many touchpoints"""
        orchestrator = JourneyOrchestrationIntelligence()
        
        # Create complex journey
        complex_journey = {
            'touchpoints': [f'touchpoint_{i}' for i in range(100)],
            'actors': [f'actor_{i}' for i in range(20)],
            'channels': ['web', 'mobile', 'email', 'phone', 'chat', 'social']
        }
        
        start_time = asyncio.get_event_loop().time()
        result = await orchestrator.analyze_journey(complex_journey)
        end_time = asyncio.get_event_loop().time()
        
        # Should complete within reasonable time
        assert (end_time - start_time) < 5.0  # 5 seconds max
        assert result is not None
    
    async def test_concurrent_journey_analysis(self):
        """Test concurrent analysis of multiple journeys"""
        orchestrator = JourneyOrchestrationIntelligence()
        
        # Create multiple journey contexts
        journeys = [
            JourneyContext(domain='customer', type=f'journey_{i}', actors=['a1', 'a2'])
            for i in range(10)
        ]
        
        # Analyze concurrently
        tasks = [orchestrator.analyze_journey(j) for j in journeys]
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 10
        assert all(r is not None for r in results)