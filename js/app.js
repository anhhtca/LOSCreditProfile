// App logic cho Review Hồ sơ Tín dụng Vinamilk (LOSCreditProfile)
document.addEventListener("DOMContentLoaded", function () {
  const data = window.VINAMILK_PROFILE_DATA;
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
    return bil.toLocaleString("vi-VN", { maximumFractionDigits: 1 }) + " tỷ VNĐ";
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
      `
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
      `
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
      `
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
          <label>Ngày cấp / Đăng ký thay đổi gần nhất:</label>
          <div class="form-control-view">${b.licenseIssueDate} (Cấp đổi: ${b.licenseLatestChangeDate})</div>
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
          <label>Kế toán trưởng / Giám đốc Tài chính:</label>
          <div class="form-control-view">${b.chiefAccountant.fullName} (${b.chiefAccountant.title})</div>
        </div>
      </div>

      <h4 style="margin: 24px 0 10px; color: var(--primary);"><i class="fas fa-user-tie"></i> 1. Người đại diện theo pháp luật</h4>
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

      <h4 style="margin: 24px 0 10px; color: var(--primary);"><i class="fas fa-chart-pie"></i> 2. Cơ cấu Cổ đông lớn (Nắm giữ $\\ge 5\\%$)</h4>
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

      <h4 style="margin: 24px 0 10px; color: var(--primary);"><i class="fas fa-sitemap"></i> 3. Công ty con / Người có liên quan tiêu biểu (Trích xuất BCTC)</h4>
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
    const y25 = f.year2025 || f.year2023;
    const y24 = f.year2024 || f.year2022;
    const it26 = f.interim2026;
    const container = document.getElementById("TabBusinessCreditReportContent");
    if (!container) return;

    container.innerHTML = `
      <div style="background: #eef2f7; padding: 12px 16px; border-radius: 6px; margin-bottom: 20px; border-left: 4px solid var(--primary);">
        <strong>Đơn vị kiểm toán độc lập:</strong> ${f.auditor} <br>
        <strong>Ý kiến kiểm toán:</strong> <span class="badge badge-success">${f.auditOpinion}</span> | <strong>Ngày ký BCTC kiểm toán 2025:</strong> ${f.auditDate} | <strong>Kỳ cập nhật:</strong> <span class="badge badge-primary">Niên độ 2025 - 2026</span>
      </div>

      <div class="form-grid-2">
        <div>
          <h4 style="margin-bottom: 10px; color: var(--primary);"><i class="fas fa-file-invoice-dollar"></i> Kết quả hoạt động kinh doanh (P&L)</h4>
          <table class="data-table">
            <thead>
              <tr>
                <th>Chỉ tiêu tài chính</th>
                <th class="text-right">Năm 2024</th>
                <th class="text-right">Năm 2025 (Kiểm toán)</th>
                <th class="text-right">6T/2026 (Soát xét)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Doanh thu thuần</strong></td>
                <td class="text-right">${formatShortBillion(y24.netRevenue)}</td>
                <td class="text-right"><strong style="color:var(--primary);">${formatShortBillion(y25.netRevenue)}</strong></td>
                <td class="text-right"><strong style="color:#218838;">${it26 ? formatShortBillion(it26.netRevenue) : '-'}</strong></td>
              </tr>
              <tr>
                <td>Giá vốn hàng bán</td>
                <td class="text-right">${formatShortBillion(36192433000000)}</td>
                <td class="text-right">${formatShortBillion(37436413000000)}</td>
                <td class="text-right">${formatShortBillion(19896000000000)}</td>
              </tr>
              <tr>
                <td><strong>Lợi nhuận gộp</strong></td>
                <td class="text-right">${formatShortBillion(y24.grossProfit)} (${y24.grossMarginPercent}%)</td>
                <td class="text-right"><strong>${formatShortBillion(y25.grossProfit)}</strong> (${y25.grossMarginPercent}%)</td>
                <td class="text-right">${it26 ? formatShortBillion(it26.grossProfit) + ' (' + it26.grossMarginPercent + '%)' : '-'}</td>
              </tr>
              <tr>
                <td>Doanh thu tài chính (Lãi tiền gửi)</td>
                <td class="text-right">${formatShortBillion(y24.financialIncome)}</td>
                <td class="text-right">${formatShortBillion(y25.financialIncome)}</td>
                <td class="text-right">${it26 ? formatShortBillion(it26.financialIncome) : '-'}</td>
              </tr>
              <tr>
                <td>Chi phí lãi vay ngân hàng</td>
                <td class="text-right">${formatShortBillion(y24.interestExpense)}</td>
                <td class="text-right">${formatShortBillion(y25.interestExpense)}</td>
                <td class="text-right">${it26 ? formatShortBillion(it26.interestExpense) : '-'}</td>
              </tr>
              <tr>
                <td><strong>Lợi nhuận trước thuế (LNTT)</strong></td>
                <td class="text-right">${formatShortBillion(y24.profitBeforeTax)}</td>
                <td class="text-right"><strong>${formatShortBillion(y25.profitBeforeTax)}</strong></td>
                <td class="text-right"><strong>${it26 ? formatShortBillion(it26.profitBeforeTax) : '-'}</strong></td>
              </tr>
              <tr style="background:#fcf1f3;">
                <td><strong>LỢI NHUẬN SAU THUẾ (LNST)</strong></td>
                <td class="text-right"><strong>${formatShortBillion(y24.profitAfterTax)}</strong></td>
                <td class="text-right"><strong style="color:var(--primary); font-size:14px;">${formatShortBillion(y25.profitAfterTax)}</strong></td>
                <td class="text-right"><strong style="color:#218838; font-size:14px;">${it26 ? formatShortBillion(it26.profitAfterTax) : '-'}</strong></td>
              </tr>
              <tr>
                <td>Lãi cơ bản trên cổ phiếu (EPS)</td>
                <td class="text-right">4.022 đ</td>
                <td class="text-right"><strong>4.028 đ</strong></td>
                <td class="text-right">2.420 đ (6T)</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div>
          <h4 style="margin-bottom: 10px; color: var(--primary);"><i class="fas fa-balance-scale"></i> Bảng cân đối kế toán & Khả năng thanh toán (2025-2026)</h4>
          <table class="data-table">
            <thead>
              <tr>
                <th>Chỉ tiêu cân đối</th>
                <th class="text-right">Giá trị (31/12/2025)</th>
                <th class="text-right">Tỷ trọng / Đánh giá</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>TỔNG TÀI SẢN</strong></td>
                <td class="text-right"><strong style="color:var(--primary);">${formatShortBillion(y25.totalAssets)}</strong></td>
                <td class="text-right">100% (Quy mô >53.000 tỷ)</td>
              </tr>
              <tr>
                <td>- Tiền & Tiền gửi ngân hàng</td>
                <td class="text-right"><strong>${formatShortBillion(y25.cashAndCashEquivalents + y25.shortTermInvestments)}</strong></td>
                <td class="text-right">43.4% TTS (Cực kỳ dồi dào)</td>
              </tr>
              <tr>
                <td>- Phải thu ngắn hạn khách hàng</td>
                <td class="text-right">${formatShortBillion(y25.shortTermReceivables)}</td>
                <td class="text-right">11.3% TTS (Quản trị tốt)</td>
              </tr>
              <tr>
                <td>- Hàng tồn kho (nguyên liệu, thành phẩm)</td>
                <td class="text-right">${formatShortBillion(y25.inventories)}</td>
                <td class="text-right">12.8% TTS (Dự trữ an toàn)</td>
              </tr>
              <tr>
                <td>- Tài sản cố định (nhà máy, trang trại)</td>
                <td class="text-right">${formatShortBillion(y25.fixedAssets)}</td>
                <td class="text-right">23.7% TTS</td>
              </tr>
              <tr>
                <td><strong>NỢ PHẢI TRẢ</strong></td>
                <td class="text-right"><strong>${formatShortBillion(y25.totalLiabilities)}</strong></td>
                <td class="text-right"><span class="badge badge-success">Nợ/TTS: ${(y25.debtToAssetsRatio * 100).toFixed(1)}% (Chuẩn AAA)</span></td>
              </tr>
              <tr>
                <td>- Vay ngắn hạn ngân hàng</td>
                <td class="text-right">${formatShortBillion(y25.shortTermBorrowings)}</td>
                <td class="text-right">Tài trợ VLĐ chu kỳ sản xuất</td>
              </tr>
              <tr>
                <td><strong>VỐN CHỦ SỞ HỮU</strong></td>
                <td class="text-right"><strong style="color:var(--primary);">${formatShortBillion(y25.equity)}</strong></td>
                <td class="text-right"><span class="badge badge-success">VCSH/TTS: 57.6%</span></td>
              </tr>
              <tr style="background:#e8f4ec;">
                <td><strong>Dòng tiền thuần HĐKD (OCF)</strong></td>
                <td class="text-right"><strong style="color:#218838;">+${formatShortBillion(y25.operatingCashFlow)}</strong></td>
                <td class="text-right"><span class="badge badge-success">Thặng dư >10.500 tỷ</span></td>
              </tr>
              <tr>
                <td><strong>Hiệu quả sinh lời ROE / ROA</strong></td>
                <td class="text-right"><strong>ROE: ${y25.roe}% | ROA: ${y25.roa}%</strong></td>
                <td class="text-right"><span class="badge badge-primary">Hiệu quả sinh lời rất cao</span></td>
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
      `
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

      <h4 style="margin-bottom: 12px; color: var(--primary);"><i class="fas fa-info-circle"></i> 2. Thông tin bổ sung & Đánh giá</h4>
      <div class="form-grid-2">
        <div class="form-group">
          <label>Xếp hạng tín dụng nội bộ Agribank:</label>
          <div class="form-control-view"><span class="badge badge-success" style="font-size:13px;">HẠNG AAA (Rủi ro cực thấp)</span></div>
        </div>
        <div class="form-group">
          <label>Lịch sử quan hệ tín dụng trên CIC:</label>
          <div class="form-control-view"><span class="badge badge-success">Nhóm 1 (Chuẩn) - Không có nợ cần chú ý hoặc nợ xấu trong lịch sử</span></div>
        </div>
        <div class="form-group">
          <label>Tổ chức đánh giá thương hiệu:</label>
          <div class="form-control-view">Brand Finance xếp hạng Top 6 thương hiệu sữa giá trị nhất toàn cầu (3 tỷ USD)</div>
        </div>
        <div class="form-group">
          <label>Chính sách ESG & Phát triển bền vững:</label>
          <div class="form-control-view">Doanh nghiệp tiên phong Net Zero 2050; 3 nhà máy & trang trại đạt trung hòa carbon quốc tế</div>
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
      `
      )
      .join("");

    container.innerHTML = `
      <div style="background: #eafaf1; padding: 14px 18px; border-radius: 6px; margin-bottom: 20px; border-left: 4px solid #28a745;">
        <h4 style="color: #218838; margin-bottom: 6px;"><i class="fas fa-stamp"></i> KẾT QUẢ PHÊ DUYỆT TÍN DỤNG VƯỢT THẨM QUYỀN</h4>
        <div>Hội đồng Thẩm định & Phê duyệt Tín dụng Trung tâm Phê duyệt Miền Nam quyết định <strong>CHẤP THUẬN CẤP HẠN MỨC TÍN DỤNG 3.000 TỶ VNĐ</strong> cho Công ty Cổ phần Sữa Việt Nam.</div>
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
        `
        )
        .join("");

      publicDocsHtml = `
        <div id="public-docs-storage" class="doc-category-box" style="border: 2px solid #28a745; margin-bottom: 24px; background: #fafdfb;">
          <div class="doc-category-header" style="background: #28a745; color: #fff;">
            <div>
              <span class="cat-title"><i class="fas fa-archive"></i> KHO HỒ SƠ THU THẬP NGUYÊN BẢN CÔNG KHAI</span> (Chính thức từ HOSE, Vinamilk IR, KPMG)
            </div>
            <span class="badge badge-light" style="color: #28a745; font-weight: bold;">${publicDocs.length} tài liệu gốc (~22 MB)</span>
          </div>
          <div style="padding: 10px 15px; font-size: 12px; color: #155724; background: #e8f5e9; border-bottom: 1px solid #c3e6cb;">
            <i class="fas fa-info-circle"></i> Toàn bộ các tài liệu dưới đây được thu thập nguyên bản từ nguồn niêm yết công khai chính thức, dùng trực tiếp thay thế bản parsed/generated để phục vụ kiểm thử OCR/AI. Đã lưu trữ cố định để xem và tải về dùng lại sau này.
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
        .map(
          (d) => {
            const folderMap = {
              "A": "A_Ho_So_Phap_Ly",
              "B": "B_Ho_So_Kinh_Te",
              "C": "C_Ho_So_Vay_Von",
              "D": "D_Ho_So_Tai_San_Bao_Dam",
              "E": "E_Ho_So_Chi_Nhanh_Lap",
              "F": "F_Ho_So_TTPD_Lap",
              "G": "G_Thong_Bao_Thu_Cong_Tac",
              "H": "H_Ho_So_Giai_Ngan",
              "I": "I_Ho_So_Quan_Ly_No"
            };
            const catFolder = folderMap[cat.code];
            const pdfPath = catFolder ? `documents/7900.001.23.DN.0300588569/${catFolder}/${d.fileName}` : null;
            return `
          <tr>
            <td width="90"><code>${d.code}</code></td>
            <td>
              <strong>${d.name}</strong>
              ${d.size ? `<br><small class="text-muted"><i class="far fa-file-alt"></i> ${d.size}</small>` : ''}
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
          }
        )
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
            <strong style="color:var(--primary);"><i class="fas fa-comment-dots"></i> Phạm Quốc Tuấn (Chuyên viên TTPD Miền Nam)</strong>
            <span class="text-muted" style="font-size:11px;">2026-04-21 10:15</span>
          </div>
          <p>Kính gửi Chi nhánh: Đề nghị Chi nhánh làm rõ cơ cấu doanh thu và dòng tiền thuần HĐKD năm 2025 (đạt 10.520 tỷ VNĐ) cùng kế hoạch giải ngân vốn lưu động phục vụ xuất khẩu trong 6 tháng đầu năm 2026 để TTPD thẩm tra dòng tiền ngoại tệ.</p>
        </div>
        <div style="background:#fdf5f7; border:1px solid var(--primary-border); border-radius:6px; padding:12px 16px; margin-left: 24px;">
          <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
            <strong style="color:#218838;"><i class="fas fa-reply"></i> Trần Thanh Phong (CBTD Agribank CN TP.HCM)</strong>
            <span class="text-muted" style="font-size:11px;">2026-04-21 15:40</span>
          </div>
          <p>Kính gửi TTPD: Chi nhánh đã làm việc với Ban Tài chính Vinamilk và cập nhật Thuyết minh BCTC kiểm toán 2025: Doanh thu thuần năm 2025 đạt 63.645,9 tỷ VNĐ (+3.0% YoY), dòng tiền kinh doanh thặng dư dồi dào, tiền và tiền gửi ngắn hạn đạt 23.150 tỷ VNĐ. Nhà cung cấp bao bì lớn nhất là Tetra Pak (Thụy Điển), bột sữa nguyên liệu từ Fonterra (New Zealand). Tài liệu chi tiết đã được tải lên tại Tab Hồ sơ đính kèm (Mục B.1 và C.I.1.3).</p>
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
                Số: 15/2026/VNM-TC<br>
                <i>V/v: Hồ sơ cấp tín dụng Agribank</i>
              </td>
              <td style="text-align: center; width: 50%; vertical-align: top; border: none; font-size: 11px;">
                <strong>CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM</strong><br>
                <u>Độc lập - Tự do - Hạnh phúc</u><br><br>
                <i>TP. Hồ Chí Minh, ngày 15 tháng 04 năm 2026</i>
              </td>
            </tr>
          </table>
        </div>

        <div style="text-align: center; margin: 25px 0 15px;">
          <h3 style="text-transform: uppercase; margin-bottom: 5px;">${name}</h3>
          <p><i>(Trích xuất từ Hồ sơ công bố thông tin chính thức của Vinamilk - Mã CK: VNM)</i></p>
        </div>

        <div style="font-size: 13px; line-height: 1.8; text-align: justify;">
          <p><strong>Căn cứ:</strong> Giấy chứng nhận đăng ký doanh nghiệp số <strong>0300588569</strong> đăng ký thay đổi lần thứ 34 do Sở KH&ĐT TP.HCM cấp ngày 25/06/2024;</p>
          <p><strong>Căn cứ:</strong> Điều lệ tổ chức và hoạt động Công ty Cổ phần Sữa Việt Nam cập nhật thông qua theo Nghị quyết ĐHĐCĐ;</p>
          <p><strong>Căn cứ:</strong> Báo cáo tài chính hợp nhất kiểm toán năm 2025 thực hiện bởi Công ty TNHH KPMG Việt Nam (Ý kiến chấp nhận toàn phần);</p>
          <p><strong>Căn cứ:</strong> Báo cáo tài chính hợp nhất bán niên soát xét 6 tháng đầu năm 2026 công bố chính thức trên HOSE.</p>
          <hr style="margin: 15px 0; border: none; border-top: 1px dashed #ccc;">
          <p><strong>Thông tin chính thức:</strong></p>
          <ul>
            <li>Tên khách hàng vay: <strong>CÔNG TY CỔ PHẦN SỮA VIỆT NAM (VINAMILK)</strong></li>
            <li>Địa chỉ: Số 10 Tân Trào, Phường Tân Phú, Quận 7, TP. Hồ Chí Minh</li>
            <li>Vốn điều lệ: <strong>20.899.554.450.000 VNĐ</strong></li>
            <li>Doanh thu thuần năm 2025 (Kiểm toán): <strong>63.645.887 triệu VNĐ</strong></li>
            <li>Lợi nhuận sau thuế năm 2025: <strong>9.413.590 triệu VNĐ</strong> (ROE: 30,67%)</li>
            <li>Doanh thu thuần lũy kế 6T/2026: <strong>34.996.005 triệu VNĐ</strong> (LNST: 5.642.623 triệu VNĐ)</li>
            <li>Tiền & Đầu tư tài chính ngắn hạn (31/12/2025): <strong>23.149.743 triệu VNĐ</strong></li>
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
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data, null, 2));
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
      const docTabBtn = document.querySelector('.tab-btn[data-tab="tab-documents"]');
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
