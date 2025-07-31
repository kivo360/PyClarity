"""
Comprehensive test suite for Project Health Diagnostic tool.

This tool analyzes project health across PMI's 10 knowledge areas,
perfect for PM/product management, engineering systems, and error reduction.
"""

import pytest
from typing import Dict, List, Any
from datetime import datetime, timedelta
import asyncio
from unittest.mock import Mock, patch, AsyncMock


class ProjectHealthDiagnostic:
    """Mock implementation for testing."""
    
    def __init__(self):
        self.integration_analyzer = IntegrationHealthAnalyzer()
        self.scope_monitor = ScopeHealthMonitor()
        self.schedule_diagnostician = ScheduleHealthDiagnostician()
        self.cost_analyzer = CostHealthAnalyzer()
        self.quality_assessor = QualityHealthAssessor()
        self.resource_optimizer = ResourceHealthOptimizer()
        self.communications_evaluator = CommunicationsHealthEvaluator()
        self.risk_scanner = RiskHealthScanner()
        self.procurement_auditor = ProcurementHealthAuditor()
        self.stakeholder_mapper = StakeholderHealthMapper()
    
    async def perform_comprehensive_diagnosis(self, project_data: Dict) -> Dict:
        """Run full health check across all knowledge areas."""
        results = await asyncio.gather(
            self.integration_analyzer.analyze_integration_health(project_data),
            self.scope_monitor.assess_scope_health(project_data),
            self.schedule_diagnostician.diagnose_schedule_health(project_data),
            self.cost_analyzer.evaluate_cost_health(project_data),
            self.quality_assessor.measure_quality_health(project_data),
            self.resource_optimizer.optimize_resource_health(project_data),
            self.communications_evaluator.evaluate_communication_health(project_data),
            self.risk_scanner.scan_risk_health(project_data),
            self.procurement_auditor.audit_procurement_health(project_data),
            self.stakeholder_mapper.map_stakeholder_health(project_data)
        )
        
        return {
            'overall_health_score': self._calculate_overall_health(results),
            'knowledge_area_scores': self._compile_area_scores(results),
            'critical_issues': self._identify_critical_issues(results),
            'improvement_recommendations': self._generate_recommendations(results),
            'trend_analysis': self._analyze_trends(results)
        }
    
    def _calculate_overall_health(self, results: List) -> float:
        """Calculate weighted overall health score."""
        scores = [r.get('score', 0) for r in results]
        return sum(scores) / len(scores) if scores else 0.0
    
    def _compile_area_scores(self, results: List) -> Dict:
        """Compile scores by knowledge area."""
        return {
            'integration': results[0].get('score', 0),
            'scope': results[1].get('score', 0),
            'schedule': results[2].get('score', 0),
            'cost': results[3].get('score', 0),
            'quality': results[4].get('score', 0),
            'resources': results[5].get('score', 0),
            'communications': results[6].get('score', 0),
            'risk': results[7].get('score', 0),
            'procurement': results[8].get('score', 0),
            'stakeholders': results[9].get('score', 0)
        }
    
    def _identify_critical_issues(self, results: List) -> List[Dict]:
        """Extract critical issues from all analyses."""
        critical_issues = []
        for result in results:
            if 'critical_issues' in result:
                critical_issues.extend(result['critical_issues'])
        return sorted(critical_issues, key=lambda x: x.get('severity', 0), reverse=True)
    
    def _generate_recommendations(self, results: List) -> List[Dict]:
        """Generate prioritized recommendations."""
        recommendations = []
        for result in results:
            if 'recommendations' in result:
                recommendations.extend(result['recommendations'])
        return sorted(recommendations, key=lambda x: x.get('impact', 0), reverse=True)
    
    def _analyze_trends(self, results: List) -> Dict:
        """Analyze health trends across time."""
        return {
            'momentum': 'improving',
            'risk_trajectory': 'stable',
            'quality_trend': 'upward',
            'resource_efficiency': 'optimizing'
        }


class IntegrationHealthAnalyzer:
    """Analyzes project integration health."""
    
    async def analyze_integration_health(self, project_data: Dict) -> Dict:
        """Analyze how well project components integrate."""
        return {
            'score': 85.5,
            'integration_points': self._map_integration_points(project_data),
            'dependency_health': self._check_dependencies(project_data),
            'process_alignment': self._assess_process_alignment(project_data),
            'critical_issues': [],
            'recommendations': [
                {'action': 'Strengthen API contracts', 'impact': 8}
            ]
        }
    
    def _map_integration_points(self, data: Dict) -> List[Dict]:
        return [{'point': 'API Gateway', 'health': 'good'}]
    
    def _check_dependencies(self, data: Dict) -> Dict:
        return {'healthy': 12, 'at_risk': 2, 'critical': 0}
    
    def _assess_process_alignment(self, data: Dict) -> float:
        return 0.87


class ScopeHealthMonitor:
    """Monitors project scope health."""
    
    async def assess_scope_health(self, project_data: Dict) -> Dict:
        """Assess scope definition and management."""
        return {
            'score': 78.2,
            'scope_clarity': self._measure_scope_clarity(project_data),
            'creep_indicators': self._detect_scope_creep(project_data),
            'completion_ratio': self._calculate_completion(project_data),
            'critical_issues': [
                {'issue': 'Undefined requirements in module X', 'severity': 6}
            ],
            'recommendations': [
                {'action': 'Clarify acceptance criteria', 'impact': 7}
            ]
        }
    
    def _measure_scope_clarity(self, data: Dict) -> float:
        return 0.75
    
    def _detect_scope_creep(self, data: Dict) -> Dict:
        return {'risk_level': 'medium', 'indicators': ['feature requests +15%']}
    
    def _calculate_completion(self, data: Dict) -> float:
        return 0.67


class ScheduleHealthDiagnostician:
    """Diagnoses schedule health and timeline risks."""
    
    async def diagnose_schedule_health(self, project_data: Dict) -> Dict:
        """Diagnose schedule adherence and risks."""
        return {
            'score': 72.8,
            'schedule_variance': self._calculate_variance(project_data),
            'critical_path_health': self._analyze_critical_path(project_data),
            'milestone_status': self._check_milestones(project_data),
            'critical_issues': [
                {'issue': 'Critical path delay of 5 days', 'severity': 8}
            ],
            'recommendations': [
                {'action': 'Fast-track testing phase', 'impact': 9}
            ]
        }
    
    def _calculate_variance(self, data: Dict) -> Dict:
        return {'days_behind': 5, 'percentage': -12.5}
    
    def _analyze_critical_path(self, data: Dict) -> Dict:
        return {'status': 'at_risk', 'buffer_days': 2}
    
    def _check_milestones(self, data: Dict) -> Dict:
        return {'completed': 4, 'upcoming': 3, 'at_risk': 1}


class CostHealthAnalyzer:
    """Analyzes project cost health and budget adherence."""
    
    async def evaluate_cost_health(self, project_data: Dict) -> Dict:
        """Evaluate cost performance and projections."""
        return {
            'score': 81.3,
            'budget_variance': self._calculate_budget_variance(project_data),
            'burn_rate_analysis': self._analyze_burn_rate(project_data),
            'cost_projections': self._project_costs(project_data),
            'critical_issues': [],
            'recommendations': [
                {'action': 'Optimize cloud resource usage', 'impact': 6}
            ]
        }
    
    def _calculate_budget_variance(self, data: Dict) -> Dict:
        return {'variance_percentage': -3.2, 'amount': -15000}
    
    def _analyze_burn_rate(self, data: Dict) -> Dict:
        return {'current_rate': 50000, 'projected_rate': 48000, 'trend': 'improving'}
    
    def _project_costs(self, data: Dict) -> Dict:
        return {'eac': 480000, 'etc': 180000, 'variance_at_completion': -20000}


class QualityHealthAssessor:
    """Assesses quality metrics and standards compliance."""
    
    async def measure_quality_health(self, project_data: Dict) -> Dict:
        """Measure quality indicators and compliance."""
        return {
            'score': 88.7,
            'defect_metrics': self._analyze_defects(project_data),
            'code_quality_score': self._assess_code_quality(project_data),
            'test_coverage': self._measure_test_coverage(project_data),
            'critical_issues': [],
            'recommendations': [
                {'action': 'Increase unit test coverage to 90%', 'impact': 5}
            ]
        }
    
    def _analyze_defects(self, data: Dict) -> Dict:
        return {'open': 23, 'closed': 145, 'critical': 2, 'trend': 'decreasing'}
    
    def _assess_code_quality(self, data: Dict) -> float:
        return 0.92
    
    def _measure_test_coverage(self, data: Dict) -> Dict:
        return {'unit': 0.85, 'integration': 0.72, 'e2e': 0.65}


class ResourceHealthOptimizer:
    """Optimizes resource allocation and utilization."""
    
    async def optimize_resource_health(self, project_data: Dict) -> Dict:
        """Analyze and optimize resource utilization."""
        return {
            'score': 76.4,
            'utilization_metrics': self._calculate_utilization(project_data),
            'skill_gap_analysis': self._analyze_skill_gaps(project_data),
            'allocation_efficiency': self._measure_allocation(project_data),
            'critical_issues': [
                {'issue': 'Senior developer overallocation', 'severity': 7}
            ],
            'recommendations': [
                {'action': 'Redistribute backend tasks', 'impact': 8}
            ]
        }
    
    def _calculate_utilization(self, data: Dict) -> Dict:
        return {'average': 0.82, 'peak': 1.15, 'optimal_range': (0.7, 0.9)}
    
    def _analyze_skill_gaps(self, data: Dict) -> List[Dict]:
        return [{'skill': 'DevOps', 'gap_severity': 'medium'}]
    
    def _measure_allocation(self, data: Dict) -> float:
        return 0.73


class CommunicationsHealthEvaluator:
    """Evaluates project communication effectiveness."""
    
    async def evaluate_communication_health(self, project_data: Dict) -> Dict:
        """Evaluate communication channels and effectiveness."""
        return {
            'score': 83.9,
            'channel_effectiveness': self._assess_channels(project_data),
            'stakeholder_engagement': self._measure_engagement(project_data),
            'information_flow': self._analyze_info_flow(project_data),
            'critical_issues': [],
            'recommendations': [
                {'action': 'Implement weekly stakeholder sync', 'impact': 6}
            ]
        }
    
    def _assess_channels(self, data: Dict) -> Dict:
        return {'email': 0.7, 'slack': 0.9, 'meetings': 0.75}
    
    def _measure_engagement(self, data: Dict) -> Dict:
        return {'score': 0.84, 'trend': 'stable'}
    
    def _analyze_info_flow(self, data: Dict) -> Dict:
        return {'bottlenecks': 1, 'latency': 'low'}


class RiskHealthScanner:
    """Scans and evaluates project risks."""
    
    async def scan_risk_health(self, project_data: Dict) -> Dict:
        """Scan for risks and evaluate mitigation."""
        return {
            'score': 79.1,
            'risk_registry': self._compile_risks(project_data),
            'mitigation_effectiveness': self._assess_mitigation(project_data),
            'emerging_risks': self._detect_emerging_risks(project_data),
            'critical_issues': [
                {'issue': 'Unmitigated technical debt risk', 'severity': 6}
            ],
            'recommendations': [
                {'action': 'Implement risk review cadence', 'impact': 7}
            ]
        }
    
    def _compile_risks(self, data: Dict) -> Dict:
        return {'high': 2, 'medium': 5, 'low': 8, 'total': 15}
    
    def _assess_mitigation(self, data: Dict) -> float:
        return 0.78
    
    def _detect_emerging_risks(self, data: Dict) -> List[Dict]:
        return [{'risk': 'Supply chain disruption', 'probability': 0.3}]


class ProcurementHealthAuditor:
    """Audits procurement and vendor management health."""
    
    async def audit_procurement_health(self, project_data: Dict) -> Dict:
        """Audit procurement processes and vendor performance."""
        return {
            'score': 85.2,
            'vendor_performance': self._evaluate_vendors(project_data),
            'contract_compliance': self._check_compliance(project_data),
            'procurement_efficiency': self._measure_efficiency(project_data),
            'critical_issues': [],
            'recommendations': [
                {'action': 'Renegotiate SLA with vendor B', 'impact': 5}
            ]
        }
    
    def _evaluate_vendors(self, data: Dict) -> Dict:
        return {'performing': 4, 'underperforming': 1, 'exceeding': 2}
    
    def _check_compliance(self, data: Dict) -> float:
        return 0.94
    
    def _measure_efficiency(self, data: Dict) -> Dict:
        return {'cycle_time_days': 12, 'cost_savings': 0.08}


class StakeholderHealthMapper:
    """Maps and evaluates stakeholder satisfaction."""
    
    async def map_stakeholder_health(self, project_data: Dict) -> Dict:
        """Map stakeholder satisfaction and engagement."""
        return {
            'score': 87.6,
            'satisfaction_matrix': self._build_satisfaction_matrix(project_data),
            'influence_mapping': self._map_influence(project_data),
            'engagement_levels': self._measure_engagement_levels(project_data),
            'critical_issues': [],
            'recommendations': [
                {'action': 'Increase exec sponsor visibility', 'impact': 6}
            ]
        }
    
    def _build_satisfaction_matrix(self, data: Dict) -> Dict:
        return {'highly_satisfied': 6, 'satisfied': 8, 'neutral': 3, 'dissatisfied': 1}
    
    def _map_influence(self, data: Dict) -> Dict:
        return {'high_influence': 4, 'medium_influence': 7, 'low_influence': 7}
    
    def _measure_engagement_levels(self, data: Dict) -> Dict:
        return {'actively_engaged': 12, 'passively_engaged': 5, 'disengaged': 1}


# Fixtures
@pytest.fixture
def project_health_diagnostic():
    """Create project health diagnostic instance."""
    return ProjectHealthDiagnostic()


@pytest.fixture
def sample_project_data():
    """Sample project data for testing."""
    return {
        'project_id': 'PROJ-2024-001',
        'name': 'Enterprise System Modernization',
        'start_date': datetime.now() - timedelta(days=90),
        'planned_end_date': datetime.now() + timedelta(days=180),
        'budget': 500000,
        'spent': 185000,
        'team_size': 12,
        'deliverables': {
            'completed': 8,
            'in_progress': 5,
            'planned': 10
        },
        'risks': [
            {'id': 'R001', 'severity': 'high', 'mitigation': 'planned'},
            {'id': 'R002', 'severity': 'medium', 'mitigation': 'active'}
        ],
        'stakeholders': [
            {'role': 'sponsor', 'satisfaction': 8},
            {'role': 'user_rep', 'satisfaction': 7}
        ]
    }


@pytest.fixture
def failing_project_data():
    """Project data representing a struggling project."""
    return {
        'project_id': 'PROJ-2024-002',
        'name': 'Legacy Migration Initiative',
        'start_date': datetime.now() - timedelta(days=180),
        'planned_end_date': datetime.now() - timedelta(days=10),
        'budget': 300000,
        'spent': 320000,
        'team_size': 8,
        'deliverables': {
            'completed': 3,
            'in_progress': 7,
            'planned': 15
        },
        'risks': [
            {'id': 'R003', 'severity': 'critical', 'mitigation': 'none'},
            {'id': 'R004', 'severity': 'high', 'mitigation': 'planned'},
            {'id': 'R005', 'severity': 'high', 'mitigation': 'none'}
        ],
        'stakeholders': [
            {'role': 'sponsor', 'satisfaction': 4},
            {'role': 'user_rep', 'satisfaction': 3}
        ]
    }


# Integration Health Tests
class TestIntegrationHealthAnalyzer:
    """Test integration health analysis capabilities."""
    
    @pytest.mark.asyncio
    async def test_analyze_integration_health(self, sample_project_data):
        """Test basic integration health analysis."""
        analyzer = IntegrationHealthAnalyzer()
        result = await analyzer.analyze_integration_health(sample_project_data)
        
        assert 'score' in result
        assert 0 <= result['score'] <= 100
        assert 'integration_points' in result
        assert 'dependency_health' in result
        assert 'process_alignment' in result
    
    @pytest.mark.asyncio
    async def test_integration_recommendations(self, sample_project_data):
        """Test integration improvement recommendations."""
        analyzer = IntegrationHealthAnalyzer()
        result = await analyzer.analyze_integration_health(sample_project_data)
        
        assert 'recommendations' in result
        assert len(result['recommendations']) > 0
        assert all('action' in rec and 'impact' in rec for rec in result['recommendations'])


# Scope Health Tests
class TestScopeHealthMonitor:
    """Test scope health monitoring capabilities."""
    
    @pytest.mark.asyncio
    async def test_assess_scope_health(self, sample_project_data):
        """Test scope health assessment."""
        monitor = ScopeHealthMonitor()
        result = await monitor.assess_scope_health(sample_project_data)
        
        assert 'score' in result
        assert 'scope_clarity' in result
        assert 'creep_indicators' in result
        assert 'completion_ratio' in result
    
    @pytest.mark.asyncio
    async def test_scope_creep_detection(self, sample_project_data):
        """Test scope creep detection."""
        monitor = ScopeHealthMonitor()
        result = await monitor.assess_scope_health(sample_project_data)
        
        creep = result['creep_indicators']
        assert 'risk_level' in creep
        assert creep['risk_level'] in ['low', 'medium', 'high', 'critical']
        assert 'indicators' in creep


# Schedule Health Tests
class TestScheduleHealthDiagnostician:
    """Test schedule health diagnosis capabilities."""
    
    @pytest.mark.asyncio
    async def test_diagnose_schedule_health(self, sample_project_data):
        """Test schedule health diagnosis."""
        diagnostician = ScheduleHealthDiagnostician()
        result = await diagnostician.diagnose_schedule_health(sample_project_data)
        
        assert 'score' in result
        assert 'schedule_variance' in result
        assert 'critical_path_health' in result
        assert 'milestone_status' in result
    
    @pytest.mark.asyncio
    async def test_critical_path_analysis(self, sample_project_data):
        """Test critical path analysis."""
        diagnostician = ScheduleHealthDiagnostician()
        result = await diagnostician.diagnose_schedule_health(sample_project_data)
        
        cp_health = result['critical_path_health']
        assert 'status' in cp_health
        assert 'buffer_days' in cp_health
        assert cp_health['status'] in ['healthy', 'at_risk', 'critical']


# Comprehensive Diagnostic Tests
class TestProjectHealthDiagnostic:
    """Test comprehensive project health diagnostic."""
    
    @pytest.mark.asyncio
    async def test_comprehensive_diagnosis(self, project_health_diagnostic, sample_project_data):
        """Test full project health diagnosis."""
        result = await project_health_diagnostic.perform_comprehensive_diagnosis(sample_project_data)
        
        assert 'overall_health_score' in result
        assert 0 <= result['overall_health_score'] <= 100
        assert 'knowledge_area_scores' in result
        assert len(result['knowledge_area_scores']) == 10
        assert 'critical_issues' in result
        assert 'improvement_recommendations' in result
        assert 'trend_analysis' in result
    
    @pytest.mark.asyncio
    async def test_failing_project_diagnosis(self, project_health_diagnostic, failing_project_data):
        """Test diagnosis of a failing project."""
        result = await project_health_diagnostic.perform_comprehensive_diagnosis(failing_project_data)
        
        # Failing project should have lower scores
        assert result['overall_health_score'] < 70
        assert len(result['critical_issues']) > 2
        assert any(issue['severity'] > 7 for issue in result['critical_issues'])
    
    @pytest.mark.asyncio
    async def test_knowledge_area_coverage(self, project_health_diagnostic, sample_project_data):
        """Test all PMI knowledge areas are covered."""
        result = await project_health_diagnostic.perform_comprehensive_diagnosis(sample_project_data)
        
        expected_areas = [
            'integration', 'scope', 'schedule', 'cost', 'quality',
            'resources', 'communications', 'risk', 'procurement', 'stakeholders'
        ]
        
        scores = result['knowledge_area_scores']
        assert all(area in scores for area in expected_areas)
        assert all(0 <= scores[area] <= 100 for area in expected_areas)
    
    @pytest.mark.asyncio
    async def test_recommendation_prioritization(self, project_health_diagnostic, sample_project_data):
        """Test recommendation prioritization by impact."""
        result = await project_health_diagnostic.perform_comprehensive_diagnosis(sample_project_data)
        
        recommendations = result['improvement_recommendations']
        assert len(recommendations) > 0
        
        # Check recommendations are sorted by impact
        impacts = [rec['impact'] for rec in recommendations]
        assert impacts == sorted(impacts, reverse=True)
    
    @pytest.mark.asyncio
    async def test_trend_analysis(self, project_health_diagnostic, sample_project_data):
        """Test project trend analysis."""
        result = await project_health_diagnostic.perform_comprehensive_diagnosis(sample_project_data)
        
        trends = result['trend_analysis']
        assert 'momentum' in trends
        assert 'risk_trajectory' in trends
        assert 'quality_trend' in trends
        assert 'resource_efficiency' in trends
    
    @pytest.mark.asyncio
    async def test_error_handling(self, project_health_diagnostic):
        """Test error handling with invalid data."""
        invalid_data = {'invalid': 'data'}
        
        result = await project_health_diagnostic.perform_comprehensive_diagnosis(invalid_data)
        
        # Should still return valid structure even with bad data
        assert 'overall_health_score' in result
        assert 'knowledge_area_scores' in result
        assert 'critical_issues' in result
    
    @pytest.mark.asyncio
    async def test_concurrent_analysis(self, project_health_diagnostic, sample_project_data):
        """Test concurrent analysis of multiple knowledge areas."""
        import time
        
        start_time = time.time()
        result = await project_health_diagnostic.perform_comprehensive_diagnosis(sample_project_data)
        end_time = time.time()
        
        # Should complete quickly due to concurrent execution
        assert (end_time - start_time) < 2.0  # Should be much faster than sequential
        assert result['overall_health_score'] > 0


# Integration Tests
class TestProjectHealthIntegration:
    """Integration tests for complete health diagnostic system."""
    
    @pytest.mark.asyncio
    async def test_multi_project_comparison(self, project_health_diagnostic, 
                                          sample_project_data, failing_project_data):
        """Test comparing health across multiple projects."""
        healthy_result = await project_health_diagnostic.perform_comprehensive_diagnosis(sample_project_data)
        failing_result = await project_health_diagnostic.perform_comprehensive_diagnosis(failing_project_data)
        
        # Healthy project should score higher
        assert healthy_result['overall_health_score'] > failing_result['overall_health_score']
        assert len(healthy_result['critical_issues']) < len(failing_result['critical_issues'])
    
    @pytest.mark.asyncio
    async def test_real_world_scenario(self, project_health_diagnostic):
        """Test with realistic project scenario."""
        real_project = {
            'project_id': 'REAL-001',
            'name': 'Product Management System',
            'start_date': datetime.now() - timedelta(days=60),
            'planned_end_date': datetime.now() + timedelta(days=120),
            'budget': 750000,
            'spent': 250000,
            'team_size': 15,
            'deliverables': {
                'completed': 12,
                'in_progress': 8,
                'planned': 25
            },
            'risks': [
                {'id': 'R-TECH-001', 'severity': 'medium', 'mitigation': 'active'},
                {'id': 'R-RES-001', 'severity': 'low', 'mitigation': 'monitored'},
                {'id': 'R-SCHED-001', 'severity': 'high', 'mitigation': 'planned'}
            ],
            'stakeholders': [
                {'role': 'sponsor', 'satisfaction': 9},
                {'role': 'product_owner', 'satisfaction': 8},
                {'role': 'tech_lead', 'satisfaction': 7},
                {'role': 'user_rep', 'satisfaction': 8}
            ],
            'quality_metrics': {
                'defects': {'critical': 0, 'major': 3, 'minor': 15},
                'test_coverage': 0.82,
                'code_quality': 0.88
            }
        }
        
        result = await project_health_diagnostic.perform_comprehensive_diagnosis(real_project)
        
        # Real project should have reasonable health
        assert 70 <= result['overall_health_score'] <= 90
        assert result['knowledge_area_scores']['quality'] > 80  # Good test coverage
        assert result['knowledge_area_scores']['stakeholders'] > 85  # High satisfaction