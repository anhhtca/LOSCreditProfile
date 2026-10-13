// App logic cho Review Hồ sơ Tín dụng Vinamilk (LOSCreditProfile)
document.addEventListener("DOMContentLoaded", function () {
  const data =
    window.VINAMILK_PROFILE_DATA ||
    (typeof vinamilkProfileData !== "undefined" ? vinamilkProfileData : null);
  if (!data) {
    console.error("Không tìm thấy dữ liệu VINAMILK_PROFILE_DATA");
    return;
  }

  // Tiện ích format tiền VNĐ
  function formatMoney(num) {
    if (num === null || num === undefined) return "-";
    return num.toLocaleString("vi-VN") + " VNĐ";
  }

  function formatShortBillion(num) {
    if (!num) return "-";
    const bil = num / 1000000000;
    return (
      bil.toLocaleString("vi-VN", { maximumFractionDigits: 1 }) + " tỷ VNĐ"
    );
  }

  // 1. Tab switching
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  tabBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const targetTab = this.getAttribute("data-tab");

      tabBtns.forEach((b) => b.classList.remove("active"));
      tabContents.forEach((c) => c.classList.remove("active"));

      this.classList.add("active");
      const targetElement = document.getElementById(targetTab);
      if (targetElement) {
        targetElement.classList.add("active");
      }
    });
  });

  // 2. Accordion toggling
  const accHeaders = document.querySelectorAll(".accordion-header");
  accHeaders.forEach((header) => {
    header.addEventListener("click", function () {
      const body = this.nextElementSibling;
      const icon = this.querySelector(".acc-icon");
      if (body.style.display === "none") {
        body.style.display = "block";
        if (icon) icon.className = "fas fa-chevron-up acc-icon";
      } else {
        body.style.display = "none";
        if (icon) icon.className = "fas fa-chevron-down acc-icon";
      }
    });
  });

  // 4. Render Tab: Thông tin pháp lý (BusinessEntity)
  function renderBusinessEntity() {
    const b = data.businessEntity;
    const container = document.getElementById("TabBusinessEntityContent");
    if (!container) return;

    let repsHtml = b.legalRepresentatives
      .map(
        (r, i) => `
        <tr>
          <td>${i + 1}</td>
          <td><strong>${r.fullName}</strong></td>
          <td>${r.title}</td>
          <td>${r.birthYear}</td>
          <td>${r.idNumber}</td>
          <td>${r.idIssueDate} (${r.idIssuePlace})</td>
          <td><span class="badge badge-primary">${r.roleInLoan}</span></td>
        </tr>
      `,
      )
      .join("");

    let shareholdersHtml = b.majorShareholders
      .map(
        (sh, i) => `
        <tr>
          <td>${i + 1}</td>
          <td><strong>${sh.name}</strong></td>
          <td><span class="badge badge-secondary">${sh.type}</span></td>
          <td class="text-right">${sh.shares.toLocaleString("vi-VN")} CP</td>
          <td class="text-right"><strong>${sh.percent.toFixed(2)}%</strong></td>
        </tr>
      `,
      )
      .join("");

    let relatedHtml = b.relatedParties
      .map(
        (rp, i) => `
        <tr>
          <td>${i + 1}</td>
          <td><strong>${rp.name}</strong></td>
          <td>${rp.relation}</td>
          <td class="text-right">${rp.ownershipPercent}%</td>
        </tr>
      `,
      )
      .join("");

    container.innerHTML = `
      <div class="form-grid-2">
        <div class="form-group">
          <label>Tên Doanh nghiệp (Bên vay):</label>
          <div class="form-control-view highlight">${b.companyName} (${b.shortName})</div>
        </div>
        <div class="form-group">
          <label>Mã chứng khoán / Sàn niêm yết:</label>
          <div class="form-control-view">${b.stockTicker}</div>
        </div>
        <div class="form-group">
          <label>Mã số doanh nghiệp / Mã số thuế:</label>
          <div class="form-control-view highlight">${b.businessLicense}</div>
        </div>
        <div class="form-group">
          <label>Ngày cấp / Đăng ký thay đổi gần nhất (Theo A.1.1):</label>
          <div class="form-control-view">${b.licenseIssueDate} (Thay đổi lần thứ 33: ${b.licenseLatestChangeDate})</div>
        </div>
        <div class="form-group" style="grid-column: span 2;">
          <label>Địa chỉ trụ sở chính:</label>
          <div class="form-control-view">${b.businessAddress}</div>
        </div>
        <div class="form-group">
          <label>Vốn điều lệ:</label>
          <div class="form-control-view highlight">${formatMoney(b.charterCapital)} (${formatShortBillion(b.charterCapital)})</div>
        </div>
        <div class="form-group">
          <label>Kế toán trưởng / Giám đốc Tài chính (Theo A.1.6):</label>
          <div class="form-control-view">${b.chiefAccountant.fullName} (${b.chiefAccountant.appointmentDecision})</div>
        </div>
      </div>

      <h4 style="margin: 24px 0 10px; color: var(--primary);"><i class="fas fa-user-tie"></i> 1. Người đại diện theo pháp luật & Chủ tịch HĐQT (Theo A.1.1, A.1.5, A.1.8, A.2.1)</h4>
      <table class="data-table">
        <thead>
          <tr>
            <th width="40">STT</th>
            <th>Họ và tên</th>
            <th>Chức vụ</th>
            <th width="70">Năm sinh</th>
            <th>Số CCCD/Hộ chiếu</th>
            <th>Ngày & Nơi cấp</th>
            <th>Vai trò trong hồ sơ vay</th>
          </tr>
        </thead>
        <tbody>${repsHtml}</tbody>
      </table>

      <h4 style="margin: 24px 0 10px; color: var(--primary);"><i class="fas fa-chart-pie"></i> 2. Cơ cấu Cổ đông lớn nắm giữ &ge; 5% (Theo BC Quản trị A.1.8 & A.1.9)</h4>
      <table class="data-table">
        <thead>
          <tr>
            <th width="40">STT</th>
            <th>Tên Cổ đông</th>
            <th>Phân loại</th>
            <th class="text-right">Số lượng cổ phần</th>
            <th class="text-right" width="120">Tỷ lệ sở hữu</th>
          </tr>
        </thead>
        <tbody>${shareholdersHtml}</tbody>
      </table>

      <h4 style="margin: 24px 0 10px; color: var(--primary);"><i class="fas fa-sitemap"></i> 3. Công ty con / Người có liên quan tiêu biểu (Theo BCTC B.1 & BC Quản trị A.1.9)</h4>
      <table class="data-table">
        <thead>
          <tr>
            <th width="40">STT</th>
            <th>Tên đơn vị liên kết</th>
            <th>Mối quan hệ</th>
            <th class="text-right" width="120">Tỷ lệ biểu quyết</th>
          </tr>
        </thead>
        <tbody>${relatedHtml}</tbody>
      </table>
    `;
  }

  // 5. Render Tab: Thông tin kinh tế (BusinessCreditReport)
  function renderBusinessCreditReport() {
    const f = data.financialReport;
    const y22 = f.year2022;
    const y23 = f.year2023;
    const agm = f.agm2026Resolution;
    const container = document.getElementById("TabBusinessCreditReportContent");
    if (!container) return;

    container.innerHTML = `
      <div style="background: #eef2f7; padding: 12px 16px; border-radius: 6px; margin-bottom: 20px; border-left: 4px solid var(--primary);">
        <strong>Đơn vị kiểm toán độc lập:</strong> ${f.auditor} <br>
        <strong>Ý kiến kiểm toán:</strong> <span class="badge badge-success">${f.auditOpinion}</span> | <strong>Mốc văn bản:</strong> <code>${f.auditDate}</code>
      </div>

      <div class="form-grid-2">
        <div>
          <h4 style="margin-bottom: 10px; color: var(--primary);"><i class="fas fa-file-invoice-dollar"></i> Kết quả HĐKD (BCTC 2022 B.1, Hồ sơ 2023 B.3/F.1 & NQ ĐHĐCĐ 2026 C.I.1.2)</h4>
          <table class="data-table">
            <thead>
              <tr>
                <th>Chỉ tiêu tài chính</th>
                <th class="text-right">Năm 2022 (B.1 VAS)</th>
                <th class="text-right">Năm 2023 (B.3 / F.1)</th>
                <th class="text-right">TH 2025 / KH 2026 (C.I.1.2)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Doanh thu thuần / Tổng DT</strong></td>
                <td class="text-right">${formatShortBillion(y22.netRevenue)}</td>
                <td class="text-right"><strong style="color:var(--primary);">${formatShortBillion(y23.netRevenue)}</strong></td>
                <td class="text-right"><strong style="color:#218838;">TH25: 63.724 tỷ<br>KH26: 66.477 tỷ</strong></td>
              </tr>
              <tr>
                <td>Giá vốn hàng bán</td>
                <td class="text-right">${formatShortBillion(y22.costOfGoodsSold)}</td>
                <td class="text-right">${formatShortBillion(y23.costOfGoodsSold)}</td>
                <td class="text-right"><small class="text-muted">Theo NQ 01/NQ-CTS.ĐHĐCĐ/2026</small></td>
              </tr>
              <tr>
                <td><strong>Lợi nhuận gộp</strong></td>
                <td class="text-right">${formatShortBillion(y22.grossProfit)} (${y22.grossMarginPercent}%)</td>
                <td class="text-right"><strong>${formatShortBillion(y23.grossProfit)}</strong> (${y23.grossMarginPercent}%)</td>
                <td class="text-right">-</td>
              </tr>
              <tr>
                <td>Doanh thu hoạt động tài chính</td>
                <td class="text-right">${formatShortBillion(y22.financialIncome)}</td>
                <td class="text-right">${formatShortBillion(y23.financialIncome)}</td>
                <td class="text-right">-</td>
              </tr>
              <tr>
                <td>Chi phí lãi vay ngân hàng</td>
                <td class="text-right">${formatShortBillion(y22.interestExpense)}</td>
                <td class="text-right">${formatShortBillion(y23.interestExpense)}</td>
                <td class="text-right">-</td>
              </tr>
              <tr>
                <td><strong>Lợi nhuận trước thuế (LNTT)</strong></td>
                <td class="text-right">${formatShortBillion(y22.profitBeforeTax)}</td>
                <td class="text-right"><strong>${formatShortBillion(y23.profitBeforeTax)}</strong></td>
                <td class="text-right"><strong>TH25: ${agm ? formatShortBillion(agm.actual2025.profitBeforeTax) : "11.650 tỷ"}<br>KH26: ${agm ? formatShortBillion(agm.plan2026.profitBeforeTax) : "12.197 tỷ"}</strong></td>
              </tr>
              <tr style="background:#fcf1f3;">
                <td><strong>LỢI NHUẬN SAU THUẾ (LNST)</strong></td>
                <td class="text-right"><strong>${formatShortBillion(y22.profitAfterTax)}</strong></td>
                <td class="text-right"><strong style="color:var(--primary); font-size:14px;">${formatShortBillion(y23.profitAfterTax)}</strong></td>
                <td class="text-right"><strong style="color:#218838; font-size:13px;">TH25: ${agm ? formatShortBillion(agm.actual2025.profitAfterTax) : "9.414 tỷ"}<br>KH26: ${agm ? formatShortBillion(agm.plan2026.profitAfterTax) : "9.828 tỷ"}</strong></td>
              </tr>
              <tr>
                <td>Lãi cơ bản trên cổ phiếu (EPS)</td>
                <td class="text-right">${y22.eps.toLocaleString("vi-VN")} đ</td>
                <td class="text-right"><strong>${y23.eps.toLocaleString("vi-VN")} đ</strong></td>
                <td class="text-right">Cổ tức TM: &ge;50% LNST</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div>
          <h4 style="margin-bottom: 10px; color: var(--primary);"><i class="fas fa-balance-scale"></i> Bảng cân đối kế toán & Chỉ số thanh toán (Theo B.1, B.3, E.2, F.1)</h4>
          <table class="data-table">
            <thead>
              <tr>
                <th>Chỉ tiêu cân đối</th>
                <th class="text-right">31/12/2022 (B.1 VAS)</th>
                <th class="text-right">31/12/2023 (B.3 / F.1)</th>
                <th class="text-right">Đánh giá / Tham chiếu</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>TỔNG TÀI SẢN</strong></td>
                <td class="text-right">${formatShortBillion(y22.totalAssets)}</td>
                <td class="text-right"><strong style="color:var(--primary);">${formatShortBillion(y23.totalAssets)}</strong></td>
                <td class="text-right">100% TTS (Tăng +9,8%)</td>
              </tr>
              <tr>
                <td>- Tiền & Tiền gửi ngắn hạn</td>
                <td class="text-right">${formatShortBillion(y22.cashAndCashEquivalents + y22.shortTermInvestments)}</td>
                <td class="text-right"><strong>${formatShortBillion(y23.cashAndCashEquivalents + y23.shortTermInvestments)}</strong></td>
                <td class="text-right">43,3% TTS (Khớp F.1: 23.047 tỷ)</td>
              </tr>
              <tr>
                <td>- Phải thu ngắn hạn</td>
                <td class="text-right">${formatShortBillion(y22.shortTermReceivables)}</td>
                <td class="text-right">${formatShortBillion(y23.shortTermReceivables)}</td>
                <td class="text-right">Khớp B.3 (6.133,52 tỷ)</td>
              </tr>
              <tr>
                <td>- Hàng tồn kho</td>
                <td class="text-right">${formatShortBillion(y22.inventories)}</td>
                <td class="text-right">${formatShortBillion(y23.inventories)}</td>
                <td class="text-right">Khớp B.3 (5.618,42 tỷ)</td>
              </tr>
              <tr>
                <td>- Tài sản cố định</td>
                <td class="text-right">${formatShortBillion(y22.fixedAssets)}</td>
                <td class="text-right">${formatShortBillion(y23.fixedAssets)}</td>
                <td class="text-right">Nhà máy & Trang trại</td>
              </tr>
              <tr>
                <td><strong>NỢ PHẢI TRẢ</strong></td>
                <td class="text-right">${formatShortBillion(y22.totalLiabilities)}</td>
                <td class="text-right"><strong>${formatShortBillion(y23.totalLiabilities)}</strong></td>
                <td class="text-right"><span class="badge badge-success">Nợ/TTS: ${(y23.debtToAssetsRatio * 100).toFixed(1)}% (Hạng AAA)</span></td>
              </tr>
              <tr>
                <td>- Vay ngắn hạn ngân hàng</td>
                <td class="text-right">${formatShortBillion(y22.shortTermBorrowings)}</td>
                <td class="text-right">${formatShortBillion(y23.shortTermBorrowings)}</td>
                <td class="text-right">Khớp CIC E.1.1 (8.440 tỷ)</td>
              </tr>
              <tr>
                <td><strong>VỐN CHỦ SỞ HỮU</strong></td>
                <td class="text-right">${formatShortBillion(y22.equity)}</td>
                <td class="text-right"><strong style="color:var(--primary);">${formatShortBillion(y23.equity)}</strong></td>
                <td class="text-right"><span class="badge badge-success">VCSH/TTS: 67,2%</span></td>
              </tr>
              <tr style="background:#e8f4ec;">
                <td><strong>Dòng tiền thuần HĐKD (OCF)</strong></td>
                <td class="text-right">+${formatShortBillion(y22.operatingCashFlow)}</td>
                <td class="text-right"><strong style="color:#218838;">+${formatShortBillion(y23.operatingCashFlow)}</strong></td>
                <td class="text-right"><span class="badge badge-success">Khớp B.1 & F.1</span></td>
              </tr>
              <tr>
                <td><strong>Thanh toán & Trả lãi (E.2 / F.1)</strong></td>
                <td class="text-right">CR: ${y22.currentRatio} | ICR: ${y22.interestCoverageRatio}x</td>
                <td class="text-right"><strong>CR: ${y23.currentRatio} | QR: ${y23.quickRatio} | ICR: ${y23.interestCoverageRatio}x</strong></td>
                <td class="text-right"><span class="badge badge-primary">ROE: ${y23.roe}% | ROA: ${y23.roa}%</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    `;
  }

  // 6. Render Tab: Phương án vay vốn (LoanPurpose)
  function renderLoanPurpose() {
    const lp = data.loanProposal;
    const container = document.getElementById("TabLoanPurposeContent");
    if (!container) return;
    container.innerHTML = `
      <div class="form-grid">
        <div class="form-group" style="grid-column: span 2;">
          <label>Mục đích sử dụng vốn vay chi tiết:</label>
          <div class="form-control-view highlight" style="line-height: 1.6;">${lp.loanPurpose}</div>
        </div>
        <div class="form-group">
          <label>Phương thức cấp tín dụng:</label>
          <div class="form-control-view">${lp.creditMethod}</div>
        </div>
        <div class="form-group">
          <label>Thời hạn duy trì hạn mức:</label>
          <div class="form-control-view"><strong>${lp.creditTermMonths} tháng</strong> (Thời hạn từng khế ước tối đa: ${lp.debtReceivingTermMax} tháng)</div>
        </div>
        <div class="form-group">
          <label>Tỷ lệ tài trợ vốn lưu động:</label>
          <div class="form-control-view">${lp.financingRatio}</div>
        </div>
        <div class="form-group">
          <label>Nguồn trả nợ cam kết:</label>
          <div class="form-control-view">${lp.repaymentSource}</div>
        </div>
      </div>
    `;
  }

  // 7. Render Tab: Tài sản bảo đảm (CollateralAsset)
  function renderCollateralAsset() {
    const assets = data.collateralAssets;
    const container = document.getElementById("TabCollateralAssetContent");
    if (!container) return;

    let rows = assets
      .map(
        (a, i) => `
        <tr>
          <td><strong>${a.code}</strong></td>
          <td><strong>${a.name}</strong><br><small class="text-muted">${a.location}</small></td>
          <td><span class="badge badge-primary">${a.type}</span></td>
          <td><small>${a.legalDocuments}</small></td>
          <td class="text-right"><strong style="color:var(--primary);">${formatShortBillion(a.appraisedValue)}</strong></td>
          <td class="text-center">${a.maxFinancingRate}%</td>
          <td class="text-right"><strong style="color:#218838;">${formatShortBillion(a.acceptedCreditValue)}</strong></td>
          <td><small>${a.insuranceStatus}</small></td>
        </tr>
      `,
      )
      .join("");

    const totalVal = assets.reduce((s, a) => s + a.appraisedValue, 0);
    const totalCredit = assets.reduce((s, a) => s + a.acceptedCreditValue, 0);

    container.innerHTML = `
      <table class="data-table">
        <thead>
          <tr>
            <th width="60">Mã TS</th>
            <th>Tên & Vị trí Tài sản</th>
            <th>Loại tài sản</th>
            <th>Hồ sơ pháp lý quyền sở hữu</th>
            <th class="text-right">Giá trị định giá</th>
            <th class="text-center" width="70">Tỷ lệ tối đa</th>
            <th class="text-right">Giá trị bảo đảm</th>
            <th>Tình trạng bảo hiểm</th>
          </tr>
        </thead>
        <tbody>
          ${rows}
          <tr style="background: #fdf5f7; font-weight: bold;">
            <td colspan="4" class="text-right">TỔNG GIÁ TRỊ TÀI SẢN BẢO ĐẢM:</td>
            <td class="text-right" style="color:var(--primary);">${formatShortBillion(totalVal)}</td>
            <td></td>
            <td class="text-right" style="color:#218838;">${formatShortBillion(totalCredit)}</td>
            <td></td>
          </tr>
        </tbody>
      </table>
    `;
  }

  // 8. Render Tab: Đề xuất vay vốn (ProposalForLoan)
  function renderProposalForLoan() {
    const lp = data.loanProposal;
    const container = document.getElementById("TabProposalForLoanContent");
    if (!container) return;
    container.innerHTML = `
      <div class="form-grid-2">
        <div class="form-group">
          <label>Số tiền đề nghị vay (Hạn mức):</label>
          <div class="form-control-view highlight">${formatMoney(lp.proposedAmount)} (${lp.proposedAmountInWords})</div>
        </div>
        <div class="form-group">
          <label>Số tiền cấp phê duyệt duyệt cấp:</label>
          <div class="form-control-view highlight" style="color:#218838;">${formatMoney(lp.approvedAmount)} (${lp.approvedAmountInWords})</div>
        </div>
        <div class="form-group">
          <label>Loại tiền vay:</label>
          <div class="form-control-view">${lp.currency}</div>
        </div>
        <div class="form-group">
          <label>Lãi suất cho vay:</label>
          <div class="form-control-view">${lp.interestRate}</div>
        </div>
        <div class="form-group" style="grid-column: span 2;">
          <label>Đánh giá hiệu quả phương án kinh doanh & khả năng thu hồi nợ:</label>
          <div class="form-control-view" style="line-height: 1.6;">
            Doanh nghiệp có vị thế số 1 thị trường sữa Việt Nam (>55% thị phần), biên lãi gộp ổn định trên 40%, doanh thu trên 60.000 tỷ VNĐ/năm.
            Dòng tiền kinh doanh hàng năm thặng dư ~10.000 tỷ VNĐ, tiền gửi ngân hàng thanh khoản cao >20.000 tỷ VNĐ.
            Khả năng hoàn trả nợ gốc và lãi vay đúng hạn là 100%, rủi ro tín dụng ở mức tối thiểu.
          </div>
        </div>
      </div>
    `;
  }

  // 9. Render Tab: Thông tin chung & bổ sung (AddtionalInformation)
  function renderAddtionalInformation() {
    const s = data.profileSummary;
    const container = document.getElementById("TabAddtionalInformationContent");
    if (!container) return;
    container.innerHTML = `
      <h4 style="margin-bottom: 12px; color: var(--primary);"><i class="fas fa-file-alt"></i> 1. Thông tin chung hồ sơ tín dụng</h4>
      <div class="form-grid-2" style="margin-bottom: 24px;">
        <div class="form-group">
          <label>Mã hồ sơ tín dụng:</label>
          <div class="form-control-view highlight">${s.code}</div>
        </div>
        <div class="form-group">
          <label>Trạng thái hồ sơ:</label>
          <div class="form-control-view"><span class="badge badge-success">${s.stateText}</span></div>
        </div>
        <div class="form-group">
          <label>Đơn vị lập hồ sơ (Chi nhánh):</label>
          <div class="form-control-view">${s.branchName} (Mã: ${s.branchCode})</div>
        </div>
        <div class="form-group">
          <label>Đơn vị phê duyệt:</label>
          <div class="form-control-view">${s.approvalCenterName}</div>
        </div>
        <div class="form-group">
          <label>Phân loại thẩm quyền:</label>
          <div class="form-control-view">${s.beyondAppraisalType}</div>
        </div>
        <div class="form-group">
          <label>Kết quả phê duyệt:</label>
          <div class="form-control-view highlight">${s.approvalResult}</div>
        </div>
        <div class="form-group">
          <label>Ngày lập hồ sơ tại Chi nhánh:</label>
          <div class="form-control-view">${s.createdDate}</div>
        </div>
        <div class="form-group">
          <label>Ngày nhận đủ hồ sơ tại TTPD:</label>
          <div class="form-control-view">${s.fulfillmentDate}</div>
        </div>
      </div>

      <h4 style="margin-bottom: 12px; color: var(--primary);"><i class="fas fa-info-circle"></i> 2. Thông tin bổ sung & Đánh giá (Theo E.1.1, E.2, B.1_2022)</h4>
      <div class="form-grid-2">
        <div class="form-group">
          <label>Xếp hạng tín dụng nội bộ Agribank (Phiếu số 89/XHTD-2023 ngày 16/04/2023):</label>
          <div class="form-control-view"><span class="badge badge-success" style="font-size:13px;">HẠNG AAA - 98,5/100 điểm (Rủi ro cực thấp)</span></div>
        </div>
        <div class="form-group">
          <label>Lịch sử quan hệ tín dụng trên CIC (Mã CIC-VNM-20230415 ngày 15/04/2023):</label>
          <div class="form-control-view"><span class="badge badge-success">Nhóm 1 (Đủ tiêu chuẩn) - Không có nợ xấu trong 60 tháng gần nhất</span></div>
        </div>
        <div class="form-group">
          <label>Tổ chức đánh giá thương hiệu (BCTN B.1_2022):</label>
          <div class="form-control-view">Brand Finance xếp hạng Top 6 thương hiệu sữa giá trị nhất toàn cầu (~2,8 - 3,0 tỷ USD)</div>
        </div>
        <div class="form-group">
          <label>Chính sách ESG & Phát triển bền vững (BCTN B.1_2022 & ĐHĐCĐ 2026):</label>
          <div class="form-control-view">Doanh nghiệp tiên phong Net Zero 2050; Hệ thống trang trại sinh thái Green Farm chuẩn GlobalG.A.P</div>
        </div>
      </div>
    `;
  }

  // 10. Render Tab: Thông tin phê duyệt TTPD (Approvement)
  function renderApprovement() {
    const conditions = data.loanConditions;
    const container = document.getElementById("TabApprovementContent");
    if (!container) return;

    let condRows = conditions
      .map(
        (c, i) => `
        <tr>
          <td width="40" class="text-center">${i + 1}</td>
          <td width="220"><span class="badge badge-primary">${c.type}</span></td>
          <td><strong>${c.content}</strong></td>
          <td width="180"><span class="badge badge-success"><i class="fas fa-check-circle"></i> ${c.status}</span></td>
        </tr>
      `,
      )
      .join("");

    container.innerHTML = `
      <div style="background: #eafaf1; padding: 14px 18px; border-radius: 6px; margin-bottom: 20px; border-left: 4px solid #28a745;">
        <h4 style="color: #218838; margin-bottom: 6px;"><i class="fas fa-stamp"></i> KẾT QUẢ PHÊ DUYỆT TÍN DỤNG VƯỢT THẨM QUYỀN (Theo F.3: 89/BB-HĐPD & F.4: 120/TB-TTPD ngày 25/04/2023)</h4>
        <div>Hội đồng Thẩm định & Phê duyệt Tín dụng Trung tâm Phê duyệt Miền Nam quyết định <strong>CHẤP THUẬN CẤP HẠN MỨC TÍN DỤNG 3.000 TỶ VNĐ</strong> cho Công ty Cổ phần Sữa Việt Nam (Tỷ lệ đồng thuận 5/5 thành viên - 100%).</div>
      </div>

      <h4 style="margin-bottom: 12px; color: var(--primary);"><i class="fas fa-tasks"></i> Danh mục Điều kiện tín dụng phê duyệt (Loan Conditions)</h4>
      <table class="data-table">
        <thead>
          <tr>
            <th>STT</th>
            <th>Giai đoạn điều kiện</th>
            <th>Nội dung điều kiện tín dụng cụ thể</th>
            <th>Trạng thái tuân thủ</th>
          </tr>
        </thead>
        <tbody>${condRows}</tbody>
      </table>
    `;
  }

  // 11. Render Tab: Hồ sơ đính kèm (DocumentList)
  function renderDocumentList() {
    const tree = data.documentTree;
    const publicDocs = data.publicDocuments || [];
    const container = document.getElementById("TabDocumentListContent");
    if (!container) return;

    // 11.1 Khối Kho tài liệu công khai đã thu thập
    let publicDocsHtml = "";
    if (publicDocs.length > 0) {
      let rows = publicDocs
        .map(
          (p, i) => `
          <tr>
            <td width="40" class="text-center">${i + 1}</td>
            <td width="110"><code>${p.code}</code></td>
            <td>
              <strong>${p.name}</strong><br>
              <small class="text-muted"><i class="fas fa-landmark"></i> Nguồn thu thập: ${p.source}</small>
            </td>
            <td class="text-center" width="100"><span class="badge badge-success">${p.pageCount} trang</span></td>
            <td class="text-right" width="90"><code>${p.size}</code></td>
            <td width="200" class="text-center">
              <div style="display: flex; gap: 6px; justify-content: center;">
                <button class="btn btn-primary btn-sm btn-view-pdf" data-path="${p.path}" data-code="${p.code}" data-name="${p.name}" style="padding: 3px 8px; font-size: 11px;">
                  <i class="fas fa-file-pdf"></i> Xem scan
                </button>
                <a href="${p.path}" download="${p.fileName}" class="btn btn-outline-primary btn-sm" style="padding: 3px 8px; font-size: 11px; text-decoration: none;">
                  <i class="fas fa-download"></i> Tải về
                </a>
              </div>
            </td>
          </tr>
        `,
        )
        .join("");

      publicDocsHtml = `
        <div id="public-docs-storage" class="doc-category-box" style="border: 2px solid #28a745; margin-bottom: 24px; background: #fafdfb;">
          <div class="doc-category-header" style="background: #28a745; color: #fff;">
            <div>
              <span class="cat-title"><i class="fas fa-archive"></i> KHO HỒ SƠ THU THẬP NGUYÊN BẢN CÔNG KHAI</span> (Chính thức từ HOSE, Vinamilk IR, KPMG)
            </div>
            <span class="badge badge-light" style="color: #28a745; font-weight: bold;">${publicDocs.length} tài liệu gốc (313 trang | 15.11 MB)</span>
          </div>
          <div style="padding: 10px 15px; font-size: 12px; color: #155724; background: #e8f5e9; border-bottom: 1px solid #c3e6cb;">
            <i class="fas fa-info-circle"></i> Toàn bộ các tài liệu dưới đây là văn bản gốc chính thức của Vinamilk (KPMG kiểm toán VAS/IFRS, Báo cáo thường niên, Báo cáo quản trị HOSE, Nghị quyết & Biên bản ĐHĐCĐ thường niên 2026). Tiêu đề, số hiệu văn bản, năm, số trang và dung lượng khớp 100% với nội dung bên trong file PDF.
          </div>
          <table class="data-table" style="margin-top: 0; border: none;">
            <thead>
              <tr>
                <th width="40" class="text-center">STT</th>
                <th>Mã HS</th>
                <th>Tên tài liệu công khai chính thức</th>
                <th class="text-center">Số trang</th>
                <th class="text-right">Dung lượng</th>
                <th class="text-center">Thao tác</th>
              </tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      `;
    }

    // 11.2 Danh mục 9 nhóm hồ sơ  A - I
    let html = publicDocsHtml;
    tree.forEach((cat) => {
      let docRows = cat.documents
        .map((d) => {
          const folderMap = {
            A: "A_Ho_So_Phap_Ly",
            B: "B_Ho_So_Kinh_Te",
            C: "C_Ho_So_Vay_Von",
            D: "D_Ho_So_Tai_San_Bao_Dam",
            E: "E_Ho_So_Chi_Nhanh_Lap",
            F: "F_Ho_So_TTPD_Lap",
            G: "G_Thong_Bao_Thu_Cong_Tac",
            H: "H_Ho_So_Giai_Ngan",
            I: "I_Ho_So_Quan_Ly_No",
          };
          const catFolder = folderMap[cat.code];
          const pdfPath = catFolder
            ? `documents/7900.001.23.DN.0300588569/${catFolder}/${d.fileName}`
            : null;
          return `
          <tr>
            <td width="90"><code>${d.code}</code></td>
            <td>
              <strong>${d.name}</strong>
              ${d.size ? `<br><small class="text-muted"><i class="far fa-file-alt"></i> ${d.size}</small>` : ""}
            </td>
            <td class="text-center" width="70"><span class="badge badge-secondary">${d.fileCount} file</span></td>
            <td><i class="far fa-file-pdf text-danger"></i> <span style="font-family: monospace; font-size: 11.5px;">${d.fileName}</span></td>
            <td width="150" class="text-center">
              ${
                d.isOfficialPublicDoc
                  ? '<span class="badge badge-success" title="Thu thập trực tiếp từ nguồn công bố thông tin chính thức HOSE/Vinamilk"><i class="fas fa-check-circle"></i> Bản gốc công khai</span>'
                  : '<span class="badge badge-warning" title="Tài liệu nội bộ ngân hàng giả lập nghiệp vụ Agribank"><i class="fas fa-robot"></i> Giả lập NH</span>'
              }
            </td>
            <td width="160" class="text-center">
              ${
                pdfPath
                  ? `<div style="display: flex; gap: 4px; justify-content: center;">
                      <button class="btn btn-primary btn-sm btn-view-pdf" data-path="${pdfPath}" data-code="${d.code}" data-name="${d.name}" style="padding: 4px 8px; font-size: 11px;">
                        <i class="fas fa-file-pdf"></i> Xem Scan
                      </button>
                      <a href="${pdfPath}" download="${d.fileName}" class="btn btn-outline-primary btn-sm" title="Tải tệp này" style="padding: 4px 8px; font-size: 11px; text-decoration: none;">
                        <i class="fas fa-download"></i>
                      </a>
                     </div>`
                  : `<button class="btn btn-outline-primary btn-sm btn-preview-doc" data-code="${d.code}" data-name="${d.name}" style="padding: 4px 10px; font-size: 11px;">
                      <i class="fas fa-eye"></i> Xem scan
                     </button>`
              }
            </td>
          </tr>
        `;
        })
        .join("");

      html += `
        <div class="doc-category-box">
          <div class="doc-category-header">
            <div><span class="cat-title">Nhóm ${cat.code}:</span> ${cat.name}</div>
            <span class="badge badge-primary">${cat.documents.length} loại tài liệu</span>
          </div>
          <table class="data-table" style="margin-top: 0; border: none;">
            <thead>
              <tr>
                <th>Mã hồ sơ</th>
                <th>Tên loại tài liệu</th>
                <th class="text-center">Số lượng</th>
                <th>File đính kèm</th>
                <th class="text-center">Nguồn gốc</th>
                <th class="text-center">Thao tác</th>
              </tr>
            </thead>
            <tbody>${docRows}</tbody>
          </table>
        </div>
      `;
    });

    container.innerHTML = html;

    // Attach click event for PDF modal
    container.querySelectorAll(".btn-view-pdf").forEach((btn) => {
      btn.addEventListener("click", function () {
        const path = this.getAttribute("data-path");
        const docCode = this.getAttribute("data-code");
        const docName = this.getAttribute("data-name");
        openPdfModal(path, docCode, docName);
      });
    });

    // Attach click event for preview
    container.querySelectorAll(".btn-preview-doc").forEach((btn) => {
      btn.addEventListener("click", function () {
        const docCode = this.getAttribute("data-code");
        const docName = this.getAttribute("data-name");
        openScanModal(docCode, docName);
      });
    });
  }

  // 12. Render Tab: Trao đổi thông tin (InformationExchange)
  function renderInformationExchange() {
    const container = document.getElementById("TabInformationExchangeContent");
    if (!container) return;
    container.innerHTML = `
      <div style="display: flex; flex-direction: column; gap: 14px;">
        <div style="background:#f8f9fa; border:1px solid #dee2e6; border-radius:6px; padding:12px 16px;">
          <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
            <strong style="color:var(--primary);"><i class="fas fa-comment-dots"></i> Đỗ Quang Vinh & Phạm Quốc Tuấn (TTPD Miền Nam - Công văn số 88/CV-TTPD tại Mục G.1)</strong>
            <span class="text-muted" style="font-size:11px;">2023-04-21 10:15</span>
          </div>
          <p>Kính gửi Chi nhánh: Đề nghị Chi nhánh làm rõ cơ cấu chi phí nguyên vật liệu nhập khẩu (bột sữa nguyên kem/tách béo từ New Zealand, Hoa Kỳ) và tỷ lệ nội địa hóa nguồn sữa tươi từ hệ thống trang trại sinh thái Green Farm của Vinamilk; đồng thời cung cấp bổ sung danh mục hợp đồng mua bán nguyên liệu lớn nhất phục vụ thẩm định hạn mức giải ngân ngoại tệ/VND.</p>
        </div>
        <div style="background:#fdf5f7; border:1px solid var(--primary-border); border-radius:6px; padding:12px 16px; margin-left: 24px;">
          <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
            <strong style="color:#218838;"><i class="fas fa-reply"></i> Nguyễn Hoàng Minh & Trần Thanh Phong (Agribank CN TP.HCM - Công văn số 52/CV-NHNo.HCM tại Mục G.2)</strong>
            <span class="text-muted" style="font-size:11px;">2023-04-21 15:40</span>
          </div>
          <p>Kính gửi TTPD: Chi nhánh đã làm việc với Ban Tài chính Vinamilk và giải trình: (1) Nguồn sữa tươi nguyên liệu trong nước từ 14 trang trại chuẩn GlobalG.A.P và nông hộ liên kết đáp ứng ~40% nhu cầu chế biến sữa nước (~1.050 tấn/ngày); (2) Nguồn bột sữa nhập khẩu (~60%) từ Fonterra (New Zealand), Hoogwegt (Hà Lan) theo hợp đồng kỳ hạn 6 tháng chốt giá cố định; (3) Bao bì tiệt trùng mua từ Tetra Pak (HĐNT số 88/2023/VNM-TETRA ngày 10/01/2023 tại mục C.I.1.3).</p>
        </div>
      </div>
    `;
  }

  // 14. Scan Preview & PDF Modal Logic
  const modal = document.getElementById("previewModal");
  const modalTitle = document.getElementById("modalDocTitle");
  const modalBody = document.getElementById("modalBody");
  const modalClose = document.getElementById("modalCloseBtn");
  const modalExternalLink = document.getElementById("modalExternalLink");

  function openPdfModal(pdfPath, code, name) {
    if (!modal || !modalBody) return;
    modalTitle.innerHTML = `<i class="fas fa-file-pdf text-danger"></i> Hồ sơ Scan: [${code}] ${name}`;
    modalBody.classList.remove("paper-mode");

    if (modalExternalLink) {
      modalExternalLink.href = pdfPath;
      modalExternalLink.style.display = "inline-flex";
    }

    modalBody.innerHTML = `
      <iframe class="pdf-viewer-frame" src="${pdfPath}#toolbar=1&navpanes=0" title="${name}">
        <div style="padding: 40px; text-align: center; color: #fff;">
          <p style="font-size: 15px; margin-bottom: 15px;">Trình duyệt không hỗ trợ nhúng trực tiếp tài liệu PDF.</p>
          <a href="${pdfPath}" target="_blank" class="btn btn-primary" style="display: inline-block;">
            <i class="fas fa-external-link-alt"></i> Mở PDF trong tab mới
          </a>
        </div>
      </iframe>
    `;

    modal.classList.add("show");
  }

  function openScanModal(code, name) {
    if (!modal || !modalBody) return;
    modalTitle.innerHTML = `<i class="fas fa-file-alt"></i> Bản xem trước: [${code}] ${name}`;
    modalBody.classList.add("paper-mode");

    if (modalExternalLink) {
      modalExternalLink.style.display = "none";
    }

    // Tạo template văn bản scan giả lập chuẩn hành chính
    modalBody.innerHTML = `
      <div class="scan-paper" style="max-width: 850px; margin: 0 auto;">
        <div style="text-align: center; margin-bottom: 20px;">
          <table style="width: 100%; border: none;">
            <tr>
              <td style="text-align: left; width: 50%; vertical-align: top; border: none; font-size: 11px;">
                <strong>CÔNG TY CỔ PHẦN SỮA VIỆT NAM</strong><br>
                Mã HS: 7900.001.23.DN.0300588569<br>
                <i>V/v: Hồ sơ cấp tín dụng Agribank</i>
              </td>
              <td style="text-align: center; width: 50%; vertical-align: top; border: none; font-size: 11px;">
                <strong>CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM</strong><br>
                <u>Độc lập - Tự do - Hạnh phúc</u><br><br>
                <i>TP. Hồ Chí Minh, ngày 15 tháng 04 năm 2023</i>
              </td>
            </tr>
          </table>
        </div>

        <div style="text-align: center; margin: 25px 0 15px;">
          <h3 style="text-transform: uppercase; margin-bottom: 5px;">${name}</h3>
          <p><i>(Trích xuất từ Hồ sơ công bố thông tin chính thức của Vinamilk - Mã CK: VNM)</i></p>
        </div>

        <div style="font-size: 13px; line-height: 1.8; text-align: justify;">
          <p><strong>Căn cứ:</strong> Giấy chứng nhận đăng ký doanh nghiệp số <strong>0300588569</strong> đăng ký thay đổi lần thứ 33 do Sở KH&ĐT TP.HCM cấp ngày 27/12/2022 (Mục A.1.1);</p>
          <p><strong>Căn cứ:</strong> Nghị quyết & Biên bản họp ĐHĐCĐ thường niên năm 2026 số <strong>01/NQ-CTS.ĐHĐCĐ/2026</strong> ngày 22/04/2026 (Mục A.1.2 & C.I.1.2);</p>
          <p><strong>Căn cứ:</strong> Báo cáo tài chính hợp nhất kiểm toán năm 2022 số <strong>22-01-00293-22-6</strong> ngày 28/02/2023 của Chi nhánh Công ty TNHH KPMG (Mục B.1) và BCTC kiểm toán năm 2023 (Mục B.3, F.1);</p>
          <hr style="margin: 15px 0; border: none; border-top: 1px dashed #ccc;">
          <p><strong>Thông tin chính thức:</strong></p>
          <ul>
            <li>Tên khách hàng vay: <strong>CÔNG TY CỔ PHẦN SỮA VIỆT NAM (VINAMILK)</strong></li>
            <li>Địa chỉ: Số 10 Tân Trào, Phường Tân Phú, Quận 7, TP. Hồ Chí Minh</li>
            <li>Vốn điều lệ: <strong>20.899.554.450.000 VNĐ</strong></li>
            <li>Doanh thu thuần năm 2022 (B.1 VAS): <strong>59.956.247 triệu VNĐ</strong> | Năm 2023 (B.3/F.1): <strong>60.374.459 triệu VNĐ</strong></li>
            <li>Lợi nhuận sau thuế năm 2022: <strong>8.577.575 triệu VNĐ</strong> | Năm 2023: <strong>9.019.467 triệu VNĐ</strong></li>
            <li>KQKD 2025 & Kế hoạch 2026 (NQ ĐHĐCĐ 2026): Tổng DT 2025 đạt <strong>63.724 tỷ VNĐ</strong> (LNST <strong>9.414 tỷ VNĐ</strong>); Kế hoạch 2026 Tổng DT <strong>66.477 tỷ VNĐ</strong> (LNST <strong>9.828 tỷ VNĐ</strong>)</li>
            <li>Đề nghị vay vốn: Hạn mức vốn lưu động <strong>3.000.000.000.000 VNĐ</strong> tại Agribank Chi nhánh TP.HCM</li>
          </ul>
        </div>

        <div style="margin-top: 50px; display: flex; justify-content: space-between; position: relative;">
          <div style="text-align: center; width: 45%;">
            <strong>KẾ TOÁN TRƯỞNG</strong><br><br><br>
            <span class="signature-ink">Lê Thành Liêm</span>
            <strong>Lê Thành Liêm</strong>
          </div>
          <div style="text-align: center; width: 45%; position: relative;">
            <strong>TỔNG GIÁM ĐỐC</strong><br><br><br>
            <span class="signature-ink">Mai Kiều Liên</span>
            <strong>Mai Kiều Liên</strong>
            <div class="stamp-seal">
              ★ CÔNG TY CỔ PHẦN ★<br>
              SỮA VIỆT NAM<br>
              MST: 0300588569<br>
              TP. HỒ CHÍ MINH
            </div>
          </div>
        </div>
      </div>
    `;

    modal.classList.add("show");
  }

  function closeModal() {
    if (modal) {
      modal.classList.remove("show");
      if (modalBody) {
        modalBody.innerHTML = "";
      }
    }
  }

  if (modalClose) {
    modalClose.addEventListener("click", closeModal);
  }
  window.addEventListener("click", (e) => {
    if (e.target === modal) closeModal();
  });
  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal && modal.classList.contains("show")) {
      closeModal();
    }
  });

  // 15. Export JSON Button
  const exportBtn = document.getElementById("btnExportJson");
  if (exportBtn) {
    exportBtn.addEventListener("click", function () {
      const dataStr =
        "data:text/json;charset=utf-8," +
        encodeURIComponent(JSON.stringify(data, null, 2));
      const downloadAnchor = document.createElement("a");
      downloadAnchor.setAttribute("href", dataStr);
      downloadAnchor.setAttribute("download", "vinamilk_profile_data.json");
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
    });
  }

  // 16. Print Button
  const printBtn = document.getElementById("btnPrintProfile");
  if (printBtn) {
    printBtn.addEventListener("click", function () {
      window.print();
    });
  }

  // 17. Button Go To Public Documents Storage
  const publicDocsBtn = document.getElementById("btnGoToPublicDocs");
  if (publicDocsBtn) {
    publicDocsBtn.addEventListener("click", function () {
      const docTabBtn = document.querySelector(
        '.tab-btn[data-tab="tab-documents"]',
      );
      if (docTabBtn) docTabBtn.click();
      const storageBox = document.getElementById("public-docs-storage");
      if (storageBox) {
        storageBox.scrollIntoView({ behavior: "smooth" });
      }
    });
  }

  // Initial calls
  renderBusinessEntity();
  renderBusinessCreditReport();
  renderLoanPurpose();
  renderCollateralAsset();
  renderProposalForLoan();
  renderAddtionalInformation();
  renderApprovement();
  renderDocumentList();
  renderInformationExchange();
});
